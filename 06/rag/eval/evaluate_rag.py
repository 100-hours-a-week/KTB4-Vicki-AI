from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import csv

from app.services.rag_service import RAGService
from app.services.vector_store_service import VectorStoreManager
from app.services.llm_service import LLMManager
from app.services.embedding_service import EmbeddingService

from eval.eval_dataset import EVAL_DATA
from eval.llm_judge import faithfulness, answer_relevancy, context_precision


def build_rag_service() -> RAGService:
    embedding_service = EmbeddingService()
    vector_store = VectorStoreManager(embedding_service)
    llm = LLMManager()
    return RAGService(vector_store, llm)


def main():
    rag = build_rag_service()
    rows = []

    for item in EVAL_DATA:
        q = item["question"]
        result = rag.answer_with_context(q, n_results=3)
        answer, contexts = result["answer"], result["context"]

        print(f"\n▶ 질문: {q}")
        print(f"  답변: {answer[:60]}...")

        scores = {
            "faithfulness": faithfulness(answer, contexts),
            "answer_relevancy": answer_relevancy(q, answer),
            "context_precision": context_precision(q, contexts),
        }
        for k, v in scores.items():
            print(f"  {k}: {v:.3f}")

        rows.append(
            {
                "question": q,
                "answer": answer,
                **{k: round(v, 4) for k, v in scores.items()},
            }
        )

    print("\n=== 평균 ===")
    for k in ("faithfulness", "answer_relevancy", "context_precision"):
        avg = sum(r[k] for r in rows) / len(rows)
        print(f"  {k}: {avg:.4f}")

    with open("ragas_result.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print("\n→ ragas_result.csv 저장 완료")


if __name__ == "__main__":
    main()
