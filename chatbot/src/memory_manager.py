# 대화 기록 관리
from langchain_core.messages import (
    trim_messages,
    HumanMessage,
    AIMessage,
)
from langchain_community.chat_message_histories import ChatMessageHistory

MAX_TOKEN = 10


class MemoryManager:
    def __init__(self):
        self.history: dict[str, ChatMessageHistory] = {}

    def _get_or_create(self, session_id: str) -> ChatMessageHistory:
        if session_id not in self.history:
            self.history[session_id] = ChatMessageHistory()
        return self.history[session_id]

    def get_messages(self, session_id: str):
        history = self._get_or_create(session_id)

        return trim_messages(
            history.messages,
            max_tokens=MAX_TOKEN,
            strategy="last",
            token_counter=len,
            include_system=True,
            start_on="human",
        )

    def add(self, session_id: str, question: str, answer: str):
        history = self._get_or_create(session_id)

        history.add_messages(
            [
                HumanMessage(content=question),
                AIMessage(content=answer),
            ]
        )

    def clear(self, session_id: str):
        self.history.pop(session_id, None)

    def clear_all(self):
        self.history.clear()
