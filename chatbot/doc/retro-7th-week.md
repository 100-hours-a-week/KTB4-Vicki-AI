## 7주차 과제 
- [x] 개인 프로젝트에 구축한 RAG 파이프라인을 LangChain 기반으로 마이그레이션해 보세요. 
- [x] 마이그레이션한 LangChain 기반 RAG 파이프라인을 FastAPI로 래핑하여 REST API로 배포해 보세요. 
- [ ] LangSmith로 체인 실행을 Tracing하고 Dataset 기반으로 평가해 보세요.

## 회고

### 배운 점

* 6주차에 직접 구현했던 RAG를 Langchain을 이용해서 구현하는 방법을 배웠다.

    * 문서 로딩
    * Chunking
    * Embedding
    * Vector Store 구축
    * Retriever 구성
    * Prompt 생성
    * LLM 호출

* LangChain 내부 구조를 이해하게 되었다.

    처음에는 Runnable, Chain, Retriever 등이 추상적으로 느껴졌다.

    프로젝트를 진행하면서

    * Runnable의 데이터 흐름
    * Prompt가 생성되는 과정
    * Retriever가 호출되는 시점
    * Message History가 저장되는 방식

    등을 코드 수준에서 이해할 수 있었다.


## 3. 어려웠던 점

### 프로젝트 구조 설계

alex-rag와 나의 6주차 코드를 보며 어떻게 프로젝트 구조를 구성할지 고민했고,

* Vector Store 관리
* RAG Chain 관리
* Message History 관리
* API

를 각각 분리하면서 유지보수가 쉬운 구조를 만들 수 있었다.

### History 관리

초기에는 LangChain의 RunnableWithMessageHistory를 적용하려 했지만, 

RAG 체인의 입력 구조와 맞지 않아 원하는 위치에 대화 기록을 주입하기 어려웠다. 

이를 해결하기 위해 세션별 History를 직접 관리하는 MemoryManager를 구현하고, 

Prompt 생성 단계에서 History를 명시적으로 전달하는 구조로 변경하였다. 

이 과정을 통해 LangChain의 Runnable 데이터 흐름과 체인의 입출력 구조를 더 깊이 이해할 수 있었다.



## 4. 아쉬운 점

아직 LangSmith Evaluation과 Gemini를 활용한 자동 평가 기능은 구현했으나 

아직 평가 프롬프트가 부족해서 그런지 점수가 거의 1이 나왔다.

추후 평가 로직을 개선해야겠다.



## 5. 느낀 점

이번 프로젝트를 통해 단순히 LangChain을 사용하는 방법보다, RAG 시스템이 어떤 구성 요소로 이루어져 있으며 각 단계가 어떤 역할을 하는지 이해할 수 있었다.

특히 Retriever와 Message History의 동작 방식을 직접 구현하면서 LLM 애플리케이션은 모델 자체뿐 아니라 검색, 데이터 관리, 파이프라인 설계가 함께 중요하다는 점을 배울 수 있었다.
