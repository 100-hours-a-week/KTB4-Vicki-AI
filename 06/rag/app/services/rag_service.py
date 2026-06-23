class RAGService:
    def __init__(self, vector_store, llm):
        self.vector_store = vector_store
        self.llm = llm

    def answer(self, query: str, n_results: int = 3) -> str:
        retrieved_chunks = self.vector_store.search_relevant_chunks(
            query, n_results=n_results
        )
        return self.llm.generate_answer(query, retrieved_chunks)

    def answer_with_context(self, query: str, n_results: int = 3) -> dict:
        retrived_chunks = self.vector_store.search_relevant_chunks(query, n_results)
        answer = self.llm.generate_answer(query, retrived_chunks)
        return {"answer": answer, "context": retrived_chunks}
