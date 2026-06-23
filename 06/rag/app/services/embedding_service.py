from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, model_name: str = "BAAI/bge-m3"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts) -> list:
        # texts: str 또는 list[str]
        return self.model.encode(texts).tolist()
