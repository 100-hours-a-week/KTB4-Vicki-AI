import chromadb

from app.utils.logging import logger
from app.services.chunk_service import Chunker


class VectorStoreManager:
    def __init__(self, embedding_service):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="test", metadata={"hnsw:space": "cosine"}
        )
        self.embedding_service = embedding_service

    def reset_collection(self):
        try:
            self.client.delete_collection(name="test")
        except Exception:
            pass

        self.collection = self.client.get_or_create_collection(
            name="test", metadata={"hnsw:space": "cosine"}
        )

        logger.info(f"컬렉션 확인: {self.collection.count()}")

    def index_document(self, doc: dict):
        chunks = Chunker.fixed_split(doc["text"], chunk_size=500)

        if not chunks:
            return
        embeddings = self.embedding_service.encode(chunks)

        self.collection.add(
            ids=[f"{doc['metadata']['source']}_{i}" for i in range(len(chunks))],
            documents=chunks,
            embeddings=embeddings,
            metadatas=[
                {
                    "source": doc["metadata"]["source"],
                    "format": doc["metadata"]["format"],
                    "chunk_index": i,
                }
                for i in range(len(chunks))
            ],
        )

        logger.info(f"컬렉션 확인: {self.collection.count()}")

    def search_relevant_chunks(self, query: str, n_results: int = 7) -> list:
        query_embedding = self.embedding_service.encode(query)
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=n_results
        )

        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]  # 유사도 점수 (ChromaDB 기준)
        ids = results.get("ids", [[]])[0]

        logger.info(
            f"[Vector Search] Query: '{query}' (Requested n={n_results}, Found={len(documents)})"
        )

        for i, (doc_id, doc, dist) in enumerate(zip(ids, documents, distances)):
            preview = doc[:50].replace("\n", " ") + "..." if len(doc) > 50 else doc
            logger.info(
                f"  └ Rank {i+1} | ID: {doc_id} | Distance: {dist:.4f} | Content: {preview}"
            )
        return results.get("documents", [[]])[0]

    def delete_documents(self, source: str):
        results = self.collection.get(where={"source": source})

        ids = results["ids"]

        if ids:
            self.collection.delete(ids=ids)

        logger.info(f"{source} 문서 삭제 완료")
        logger.info(f"컬렉션 수 : {self.get_collection_count()}")

    def get_collection_count(self):
        return self.collection.count()
