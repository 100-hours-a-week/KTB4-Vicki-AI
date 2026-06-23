# RAG Project

문서 기반 질의응답(RAG, Retrieval-Augmented Generation) 시스템을 구현한 프로젝트입니다.

FastAPI를 기반으로 API 서버를 구축하고, 문서 임베딩 및 벡터 검색을 통해 LLM이 문서 내용을 바탕으로 답변을 생성할 수 있도록 구현했습니다.

---

# 프로젝트 목표

* 다양한 문서(PDF, DOCX, TXT, HTML 등)를 벡터 DB에 저장
* 사용자 질문과 관련된 문서를 검색
* 검색된 문서를 근거로 LLM이 답변 생성
* RAGAS를 활용한 성능 평가 수행
* 임베딩 모델 및 검색 파라미터 튜닝을 통한 성능 개선

---

# 기술 스택

## Backend

* FastAPI
* Python

## Vector Database

* ChromaDB

## Embedding Model

* BAAI/bge-m3

## LLM

* Ollama gemma4:e2b

## Evaluation

* RAGAS

## Document Processing

* Docling
* Python 표준 라이브러리

---

# 프로젝트 구조

```text
rag-project/
│
├── app/
│   ├── core/
│   │   └── lifespan.py
│   │
│   ├── routers/
│   │   └── chat_router.py
│   │   └── file_router.py
│   │
│   ├── models/
│   │   └── chat_model.py
│   │
│   ├── services/
│   │   ├── chunk_service.py
│   │   ├── document_loader.py
│   │   ├── embedding_service.py
│   │   ├── file_storage_service.py
│   │   ├── vector_store_service.py
│   │   ├── llm_service.py
│   │   └── rag_service.py
│   │
│   ├── utils/
│   │   └── logging.py
│   │
│   └── main.py
│
├── data/
│
├── chroma_db/
│
├── eval/
│   ├── eval_dataset.py
│   ├── evaluate_rag.py
│   └── llm_judge.py
│
├── logs/
│
└── ragas_result.csv
```

---

# 시스템 아키텍처

## 문서 적재 파이프라인

```text
문서 업로드
      ↓
Document Loader
      ↓
Chunking
      ↓
Embedding
      ↓
ChromaDB 저장
```

지원 문서 형식

* PDF
* DOCX
* TXT
* HTML
* CSV
* JSON
* Markdown

---

## 질의응답 파이프라인

```text
사용자 질문
      ↓
질문 임베딩
      ↓
ChromaDB 검색
      ↓
관련 문서 추출
      ↓
LLM
      ↓
최종 답변 생성
```

---


# API 예시

## 질문 요청

```http
POST /rag/query
```

Request

```json
{
  "question": "어댑터즈의 5단 분석법은 무엇인가요?"
}
```

Response

```json
{
  "answer": "어댑터즈의 5단 분석법은..."
}
```

---

# 성능 평가

본 프로젝트는 RAGAS를 활용하여 RAG 파이프라인 성능을 평가했습니다.

평가 지표

* Faithfulness
* Answer Relevancy
* Context Precision

---

## 평가 결과 예시

| Metric            | Score |
| ----------------- | ----- |
| Faithfulness      | 0.80  |
| Answer Relevancy  | 0.98  |
| Context Precision | 0.67  |

### 결과 분석

* 질문에 대한 답변 생성 성능은 우수
* 검색된 문서를 기반으로 답변 생성 가능
* 일부 질문에서 문서에 없는 내용을 생성하는 Hallucination 발생
* 검색 결과에 불필요한 Chunk가 포함되는 문제 확인

---

# 트러블 슈팅

## 1. 한국어 검색 성능 저하

### 문제

영어 중심 임베딩 모델 사용 시 검색 품질이 낮고 관련 없는 답변 생성

### 해결

기존 모델

```text
all-MiniLM-L6-v2
```

↓

변경

```text
BAAI/bge-m3
```

### 결과

* 한국어 검색 정확도 향상
* 검색 성공률 증가
* 답변 품질 개선

---

## 2. PDF 텍스트 추출 품질 문제

### 문제

일부 PDF에서 텍스트 추출 품질 저하

### 원인

문서 구조와 PDF 포맷 차이로 인한 추출 오류

### 해결 방향

* PDF 전용 로더 개선
* OCR 적용 검토
* 문서 전처리 강화

---

## 3. RAGAS 점수 저하

### 문제

Faithfulness와 Context Precision 점수가 낮게 측정됨

### 원인

* 검색 품질 부족
* Chunk 설정 미최적화
* Top-k 검색 범위 과다

### 개선 방향

* Chunk Size 튜닝
* Chunk Overlap 튜닝
* Retriever 최적화
* Re-ranking 적용 검토

---

# 향후 개선 사항

* Hybrid Search(BM25 + Vector Search)
* Re-ranking 적용
* Query Expansion
* Metadata Filtering
* 평가 데이터셋 확대
* 검색 근거(Source Citation) 제공
* Streaming 응답 지원
* 다중 문서 검색 성능 개선

---
# 프로젝트를 통해 배운 점
먼저, RAG 품질은 LLM보다 Retriever가 더 중요할 수 있다는 것을 느꼈다.
초기에는 답변 품질 문제를 LLM 문제로 생각했지만, 실제로는 검색 품질이 전체 성능에 큰 영향을 미쳤다.

그리고 한국어 RAG에서는 임베딩 모델 선택이 중요하다는 것도 느꼈다.
영어 중심 임베딩 모델보다 BAAI/bge-m3를 적용했을 때 검색 성능이 크게 향상되었다.

RAGAS를 활용하여 RAG를 평가해 봤는데

* Faithfulness
* Answer Relevancy
* Context Precision

을 측정함으로써 검색 문제인지, 생성 문제인지, 데이터 문제인지 구분할 수 있었다.

마지막으로 의존성 관리는 프로젝트 안정성에 큰 영향을 준다는 걸 제일 많이 느꼈다.
특히 RAGAS를 설치할 때 문제가 많이 발생했다. 
계속해서 `No module named 'langchain_community.chat_models.vertexai` 에러가 났었고
그래서 관련 langchain-community 버전을 0.3.7로 내렸다. 

내리는 과정에서도 RAGAS, LangChain, Transformers 등의 라이브러리는 버전 간 호환성 문제가 자주 발생한다는 것을 알게 되었다.


