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

# (위 01TermFrequncy.py의 import 및 공통 함수 부분 동일하게 포함)

def search_tfidf(query, inverted_index, total_docs):
    """TF-IDF 스코어링 기반 검색을 수행합니다."""
    query_tokens = preprocess_text(query)
    scores = defaultdict(float)
    
    for token in query_tokens:
        if token in inverted_index:
            df = len(inverted_index[token])
            idf = math.log2(total_docs / df) # 밑이 2인 로그 사용
            
            for doc_id, tf in inverted_index[token].items():
                if tf > 0:
                    w_td = 1 + math.log(tf) # 밑이 e인 자연로그 사용
                    scores[doc_id] += w_td * idf
                    
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
        # 함수 호출부는 각 스크립트에 맞게 유지
        results = search_tfidf(q, inverted_index, total_docs) 
        for rank, (doc_id, score) in enumerate(results, 1):
            print(f"Rank {rank}: DocID {doc_id}, Score {score:.4f}")