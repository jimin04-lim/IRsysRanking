import nltk
import pandas as pd
import re
import math
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def preprocess_text(text):
    """소문자 변환, 문장 부호 제거, 토큰화, 불용어 제거, 표제어 추출을 수행합니다."""
    text = str(text).lower()
    text = re.sub(r'[.,\-;:\'"]', ' ', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and t.isalnum()]
    return lemmas

def load_and_merge_data(xml_file):
    """Pandas를 사용하여 XML을 파싱하고 질문과 답변을 하나의 문서로 병합합니다."""
    df = pd.read_xml(xml_file)
    
    # 1. 질문(PostTypeId=1)과 답변(PostTypeId=2) 분리
    questions = df[df['PostTypeId'] == 1].copy()
    answers = df[df['PostTypeId'] == 2].copy()
    
    # 2. 답변들을 ParentId 기준으로 묶어서 'Body' 텍스트 병합
    answers_grouped = answers.groupby('ParentId')['Body'].apply(
        lambda x: ' '.join(x.dropna().astype(str))
    ).reset_index()
    answers_grouped.rename(columns={'Body': 'AnswersBody'}, inplace=True)
    
    # 3. 질문에 병합된 답변을 Left Join (질문 Id = 답변 ParentId)
    merged = pd.merge(questions, answers_grouped, left_on='Id', right_on='ParentId', how='left')
    
    # 4. 결측치(NaN)를 빈 문자열로 안전하게 처리
    merged['Title'] = merged['Title'].fillna('')
    merged['Body'] = merged['Body'].fillna('')
    merged['AnswersBody'] = merged['AnswersBody'].fillna('')
    
    docs = {}
    for _, row in merged.iterrows():
        doc_id = int(row['Id'])
        # 5. 요구사항 충족: 하나의 질문 posting에 대한 제목, 본문, 모든 답변을 합침
        content = f"{row['Title']} {row['Body']} {row['AnswersBody']}"
        docs[doc_id] = preprocess_text(content)
        
    return docs

def build_inverted_index(docs):
    """Inverted Index를 생성합니다."""
    inverted_index = defaultdict(lambda: defaultdict(int))
    for doc_id, tokens in docs.items():
        for token in tokens:
            inverted_index[token][doc_id] += 1
    return inverted_index

# (위의 import 및 공통 함수 부분 동일하게 포함)

def get_tfidf_weights(query_tokens, inverted_index, total_docs):
    """벡터 공간 모델을 위한 문서별 차원 가중치(TF-IDF)를 추출합니다."""
    doc_vectors = defaultdict(lambda: defaultdict(float))
    query_vector = defaultdict(float)
    
    for token in query_tokens:
        # 쿼리 벡터는 단순 등장 여부(TF=1)로 계산 (논의에 따라 단순화)
        if token in inverted_index:
            df = len(inverted_index[token])
            idf = math.log2(total_docs / df)
            query_vector[token] = 1.0 * idf
            
            for doc_id, tf in inverted_index[token].items():
                w_td = 1 + math.log(tf)
                doc_vectors[doc_id][token] = w_td * idf
                
    return query_vector, doc_vectors

def search_vsm(query, inverted_index, total_docs, metric='cosine'):
    query_tokens = preprocess_text(query)
    query_vector, doc_vectors = get_tfidf_weights(query_tokens, inverted_index, total_docs)
    
    scores = {}
    
    # 쿼리 벡터 크기 계산
    q_norm = math.sqrt(sum(v**2 for v in query_vector.values()))
    if q_norm == 0:
        return

    for doc_id, vector in doc_vectors.items():
        if metric == 'euclidean':
            dist_sq = 0
            for token in query_tokens:
                q_val = query_vector.get(token, 0)
                d_val = vector.get(token, 0)
                dist_sq += (q_val - d_val)**2
            scores[doc_id] = math.sqrt(dist_sq)
            
        elif metric == 'cosine':
            dot_product = 0
            d_norm_sq = 0
            for token in query_tokens:
                q_val = query_vector.get(token, 0)
                d_val = vector.get(token, 0)
                dot_product += q_val * d_val
                d_norm_sq += d_val**2
                
            d_norm = math.sqrt(d_norm_sq)
            if d_norm > 0:
                scores[doc_id] = dot_product / (q_norm * d_norm)
            else:
                scores[doc_id] = 0

    if metric == 'euclidean':
        # 거리는 짧을수록 좋으므로 오름차순
        ranked_docs = sorted(scores.items(), key=lambda x: x[1])
    else:
        # 코사인 유사도는 클수록 좋으므로 내림차순
        ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
    return ranked_docs[:5]

if __name__ == "__main__":
    print("데이터 파싱 및 역색인 구축 중...")
    docs = load_and_merge_data('Posts.xml')
    inverted_index = build_inverted_index(docs)
    total_docs = len(docs)
    
    # 과제 명세 Table 1에 맞게 쿼리 리스트를 채워주세요 (예시 추가)
    queries = ["black coffee", "espresso machine"] 
    
    for q in queries:
        print(f"\n[Query]: {q}")

        print("--- Cosine Similarity ---")
        # 수정됨: search_vsm 호출 및 코사인 지정
        results_cos = search_vsm(q, inverted_index, total_docs, metric='cosine') 
        for rank, (doc_id, score) in enumerate(results_cos, 1):
            print(f"Rank {rank}: DocID {doc_id}, Score {score:.4f}")

        print("--- Euclidean Distance ---")
        # 수정됨: search_vsm 호출 및 유클리디안 지정
        results_euc = search_vsm(q, inverted_index, total_docs, metric='euclidean') 
        for rank, (doc_id, score) in enumerate(results_euc, 1):
            print(f"Rank {rank}: DocID {doc_id}, Score {score:.4f}")