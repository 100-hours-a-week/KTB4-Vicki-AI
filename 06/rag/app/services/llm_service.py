import ollama


class LLMManager:
    def __init__(self, model_name: str = "gemma4:e2b"):
        self.model_name = model_name

    def generate_answer(self, query: str, retrieved_chunks: list) -> str:
        context = ""
        for i, chunk in enumerate(retrieved_chunks, 1):
            context += f"\n[문서 {i}]\n{chunk}\n"

        prompt = f"""다음 문서를 참고하여 질문에 한국어로 답하세요.
        문서에 없는 내용은 '제공된 문서에서 해당 정보를 찾을 수 없습니다'라고 답하세요.

        {context}

        질문: {query}"""

        response = ollama.chat(
            model=self.model_name, messages=[{"role": "user", "content": prompt}]
        )
        return response.message.content
