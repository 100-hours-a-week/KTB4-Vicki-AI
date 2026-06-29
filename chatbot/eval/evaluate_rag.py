import os

from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from src.rag_manager import RAGManager

load_dotenv()

client = Client()

DATASET_NAME = "rag-eval-dataset"

examples = [
    {
        "question": "LangChain이란?",
        "answer": "LLM 애플리케이션을 개발하기 위한 오픈소스 프레임워크입니다.",
    },
    {
        "question": "LCEL이 무엇인가요?",
        "answer": "Runnable을 파이프(|) 연산자로 연결해 체인을 구성하는 LangChain의 표현 언어입니다.",
    },
    {
        "question": "PromptTemplate의 역할은?",
        "answer": "변수를 포함한 프롬프트를 템플릿으로 관리하고 실행 시 값을 채워 완성된 프롬프트를 생성합니다.",
    },
    {
        "question": "ChatPromptTemplate은 언제 사용하나요?",
        "answer": "System, Human, AI 메시지를 포함하는 채팅용 프롬프트를 만들 때 사용합니다.",
    },
    {
        "question": "FewShotPromptTemplate의 목적은?",
        "answer": "입출력 예시를 프롬프트에 포함해 응답 형식과 패턴을 일관되게 유도합니다.",
    },
    {
        "question": "MessagesPlaceholder는 무엇인가요?",
        "answer": "실행 시점에 대화 이력을 프롬프트에 삽입할 위치를 지정합니다.",
    },
    {
        "question": "Structured Output의 장점은?",
        "answer": "LLM 응답을 미리 정의한 스키마에 맞는 구조화된 데이터로 받아 후처리를 쉽게 합니다.",
    },
    {
        "question": "JsonOutputParser는 무엇을 하나요?",
        "answer": "LLM의 텍스트 응답을 JSON 형태의 Python 딕셔너리로 변환합니다.",
    },
    {
        "question": "PydanticOutputParser의 장점은?",
        "answer": "응답을 Pydantic 객체로 변환하여 타입 검증과 필드 접근을 제공합니다.",
    },
    {
        "question": "RunnablePassthrough는 언제 사용하나요?",
        "answer": "입력을 그대로 전달하거나 assign()으로 새로운 값을 추가할 때 사용합니다.",
    },
    {
        "question": "RunnableParallel의 특징은?",
        "answer": "동일한 입력으로 여러 Runnable을 동시에 실행하고 결과를 하나의 딕셔너리로 반환합니다.",
    },
    {
        "question": "RunnableBranch는 어떤 역할을 하나요?",
        "answer": "조건에 따라 서로 다른 Runnable을 실행하도록 분기합니다.",
    },
    {
        "question": "RunnableWithMessageHistory의 역할은?",
        "answer": "세션별 대화 이력을 자동으로 불러오고 저장하여 멀티턴 대화를 지원합니다.",
    },
    {
        "question": "Document 객체란?",
        "answer": "문서 내용과 메타데이터를 함께 저장하는 LangChain의 기본 문서 단위입니다.",
    },
    {
        "question": "TextLoader는 어떤 파일을 읽나요?",
        "answer": ".txt나 .md 같은 텍스트 파일을 Document 객체로 변환합니다.",
    },
    {
        "question": "PyPDFLoader는 무엇을 하나요?",
        "answer": "PDF를 읽어 페이지 단위의 Document 객체로 변환합니다.",
    },
    {
        "question": "WebBaseLoader의 역할은?",
        "answer": "웹 페이지를 가져와 본문을 추출하고 Document 객체로 변환합니다.",
    },
]


def create_dataset():
    if client.has_dataset(dataset_name=DATASET_NAME):
        print("dataset already exists")
        return client.read_dataset(dataset_name=DATASET_NAME)

    dataset = client.create_dataset(dataset_name=DATASET_NAME)

    for e in examples:
        client.create_example(
            dataset_id=dataset.id,
            inputs={"question": e["question"]},
            outputs={"answer": e["answer"]},
        )

    return dataset


manager = RAGManager()
rag = manager.executor


def target(inputs):
    answer = rag.invoke({"question": inputs["question"], "history": []})
    return {"answer": answer}


llm = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

JUDGE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "당신은 답변 품질을 평가하는 채점자입니다.\n"
            "아래 기대 답변(reference)과 모델 답변(prediction)을 비교하고,\n"
            "의미가 일치하면 1, 부분적으로만 일치하면 0.5, 무관하면 0을 점수로 매기세요.\n"
            "응답은 반드시 첫 줄에 0/0.5/1 중 하나의 숫자만, 둘째 줄부터 짧은 이유를 적으세요.",
        ),
        (
            "human",
            "질문: {question}\n\n기대 답변: {reference}\n\n모델 답변: {prediction}",
        ),
    ]
)

judge_chain = JUDGE_PROMPT | llm | StrOutputParser()


def llm_judge(run, example):
    reply = judge_chain.invoke(
        {
            "question": example.inputs["question"],
            "reference": example.outputs["answer"],
            "prediction": run.outputs["answer"],
        }
    )
    first_line = reply.strip().splitlines()[0].strip()
    try:
        score = float(first_line)
    except ValueError:
        score = 0
    return {"key": "llm_judge_semantic_match", "score": score, "comment": reply}


if __name__ == "__main__":
    create_dataset()
    results = client.evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[llm_judge],
        experiment_prefix="rag-semantic-eval",
    )
    print(results)
