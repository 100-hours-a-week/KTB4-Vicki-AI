# RAG 시스템 진입점

import os
import logging
from operator import itemgetter

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from src.memory_manager import MemoryManager
from src.vector_store_manager import VectorStoreManager

logger = logging.getLogger(__name__)


def build_llm():
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    logger.info("==== build LLM ====")
    logger.info(f"llm provider: {provider}")

    if provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash"),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
    return ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "gemma4:e2b-mlx"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )


class RAGManager:
    def __init__(self):
        self.memory = MemoryManager()
        self.vector = VectorStoreManager()
        self.executor = self._initialize_rag_chain()

    def _initialize_rag_chain(self):

        logger.info("initialize rag")

        retriever = self.vector.get_retriever()

        def format_docs(docs):
            return "\n\n".join(d.page_content for d in docs)

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "다음 문서를 근거로 사용자 질문에 답하세요. "
                    "사용자가 이전 질문을 묻는 경우, 반드시 history에 실제로 있는 HumanMessage만을 "
                    "실제 질문으로 간주하고, 문서(context) 안에 등장하는 예시 질문은 "
                    "사용자의 질문으로 취급하지 마세요."
                    "답변에 수학적 수식 기호(예: $, $$, \times)나 복잡한 행렬 표기법을 사용하지 마세요."
                    "전문적인 수학 기호 대신 '1행 1열의 원소', '곱해서 더한다'와 같이 쉬운 한글 문장과 일반 숫자로 풀어서 설명하세요."
                    "근거가 부족하면 '주어진 자료에서는 확인할 수 없습니다.'라고 답하세요.  \n\n"
                    "{context}",
                ),
                MessagesPlaceholder(variable_name="history", optional=True),
                ("human", "{question}"),
            ]
        )

        llm = build_llm()

        rag = (
            {
                "context": itemgetter("question")
                | retriever
                | RunnableLambda(format_docs),
                "question": itemgetter("question"),
                "history": itemgetter("history"),
            }
            | prompt
            | llm
            | StrOutputParser()
        )

        return rag

    def ask(self, question: str, session_id: str) -> str:
        history = self.memory.get_messages(session_id)

        answer = self.executor.invoke(
            {"question": question, "history": history},
            config={
                "configurable": {"session_id": session_id},
                "run_name": "RAG_Main_Chain",
            },
        )

        self.memory.add(session_id, question, answer)
        return answer
