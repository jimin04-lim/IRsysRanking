import sys
import nltk
import pandas as pd
import re
import math
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# 소문자 변환, 문장 부호 제거, 토큰화, 불용어 제거, 표제어 추출을 수행
def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'[.,\-;:\'"]', ' ', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and t.isalnum()]
    return lemmas

# Pandas를 사용하여 XML을 파싱하고 질문과 답변을 하나의 문서로 병합
def load_and_merge_data(xml_file):

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

# Inverted Index를 생성
def build_inverted_index(docs):
    inverted_index = defaultdict(lambda: defaultdict(int))
    for doc_id, tokens in docs.items():
        for token in tokens:
            inverted_index[token][doc_id] += 1
    return inverted_index

# 단순 TF 기반 검색을 수행
def search_tf(query, inverted_index):
    query_tokens = preprocess_text(query)
    scores = defaultdict(int)
    
    for token in query_tokens:
        if token in inverted_index:
            for doc_id, tf in inverted_index[token].items():
                scores[doc_id] += tf
                
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_docs[:5]

if __name__ == "__main__":
    # 1. 커맨드 라인으로 쿼리 입력받기
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("검색할 쿼리 입력: ")

    print("데이터 수집중...")
    docs = load_and_merge_data('Posts.xml')
    inverted_index = build_inverted_index(docs)
    
    # 입력받은 쿼리 전처리 (소문자화, 불용어 제거 등)
    query_tokens = preprocess_text(query)
    
    # 2. 쿼리 Term들의 Inverted Index (출현 횟수) 출력
    print("\n" + "="*50)
    print(f"[Query Terms Inverted Index]")
    
    # 쿼리 내 중복 단어 출력을 방지하기 위해 set() 사용
    unique_tokens = set(query_tokens)
    if not unique_tokens:
        print("Error: 유효한 검색어 없음")
    else:
        for token in unique_tokens:
            if token in inverted_index:
                # 딕셔너리 형태로 가독성 좋게 출력: {DocID: TF 빈도, ...}
                posting_list = dict(inverted_index[token])
                print(f" - '{token}': {posting_list}")
            else:
                print(f" - '{token}': 역색인 사전에 존재하지 않습니다.")
    print("="*50)

    # 3. 문서 랭킹 순서 및 점수 출력
    print(f"\n[Ranking Result-5]: '{query}'")
    results = search_tf(query, inverted_index) 
    
    if not results:
        print("일치하는 문서가 없습니다.")
    else:
        for rank, (doc_id, score) in enumerate(results, 1):
            print(f"Rank {rank}: DocID {doc_id}, Score {score}")
            
        print("\n[Ranking Doc Contents]")
        for rank, (doc_id, score) in enumerate(results, 1):
                
            # docs[doc_id]에는 이미 전처리(토큰화, 불용어제거 등)가 완료된 리스트가 들어있습니다.
            tokenized_words = docs[doc_id]
                
            # 앞 20개의 토큰만 추출하여 공백으로 연결
            truncated_content = " ".join(tokenized_words[:20])
                
            # 전체 토큰이 20개가 넘으면 뒤에 생략 기호(...) 추가
            if len(tokenized_words) > 20:
                truncated_content += " ..."
                    
            print(f"Rank {rank}, DocID {doc_id}'s contents: \n{truncated_content}")