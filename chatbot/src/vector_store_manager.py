# Vector DB 관련 작업
#   - Document loading
#   - Chunking
#   - Embedding
#   - Chroma 생성
#   - Retriever 생성

import os
import shutil
from pathlib import Path

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    BSHTMLLoader,
)

BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH = BASE_DIR / "data" / "rag-data"
CHROMA_DIR = BASE_DIR / "chroma_db"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3


class VectorStoreManager:
    def __init__(self):
        self.embedding = OllamaEmbeddings(model="bge-m3")
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
        )

    def _load_documents(self):
        docs = []

        for file in FILE_PATH.rglob("*"):

            print(f"loading {file.name}")
            _, ext = os.path.splitext(str(file).lower())

            if ext == ".pdf":
                loader = PyPDFLoader(str(file))
            elif ext in (".txt", ".md"):
                loader = TextLoader(str(file), encoding="utf-8")
            elif ext == ".html":
                loader = BSHTMLLoader(str(file))
            else:
                print(f"Skip {file.name}")
                continue

            docs.extend(loader.load())

        return docs

    def _split_documents(self, docs):
        chunks = self.splitter.split_documents(docs)

        print(f"Split into {len(chunks)} chunks")

        return chunks

    def build_vectorstore(self):
        if CHROMA_DIR.exists():

            print("delete preexits database")

            shutil.rmtree(CHROMA_DIR)

        docs = self._load_documents()
        chunks = self._split_documents(docs)

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding,
            persist_directory=str(CHROMA_DIR),
        )

        print("Vector DB created")

        return vectorstore

    def load_vectorstore(self):
        if not CHROMA_DIR.exists():
            raise FileNotFoundError(f"Vector DB not found.")
        return Chroma(
            persist_directory=str(CHROMA_DIR), embedding_function=self.embedding
        )

    def get_retriever(self):
        vectorstore = self.load_vectorstore()
        dense = vectorstore.as_retriever(search_kwargs={"k": TOP_K})

        docs = self._load_documents()
        chunks = self._split_documents(docs)

        sparse = BM25Retriever.from_documents(chunks)
        sparse.k = TOP_K

        return EnsembleRetriever(retrievers=[dense, sparse], weights=[0.5, 0.5])
