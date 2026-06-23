# eval/llm_judge.py
import json
import re
import ollama

JUDGE_MODEL = "gemma4:e2b"


def _ask_json(prompt: str, model: str = JUDGE_MODEL, retries: int = 2) -> dict:
    """ollama에 JSON 응답을 강제하고 안전하게 파싱. 실패 시 재시도."""
    for attempt in range(retries + 1):
        resp = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            format="json",  # ← Ollama에 JSON 출력 강제
            options={"temperature": 0.0},
        )
        text = resp.message.content.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # 혹시 텍스트에 섞여 나오면 중괄호 블록만 추출
            m = re.search(r"\{.*\}", text, re.DOTALL)
            if m:
                try:
                    return json.loads(m.group())
                except json.JSONDecodeError:
                    pass
    raise ValueError(f"JSON 파싱 실패 (마지막 응답): {text[:200]}")


def faithfulness(answer: str, contexts: list[str]) -> float:
    """답변의 각 문장이 검색된 문서로 뒷받침되는 비율 (0~1)."""
    ctx = "\n".join(f"[문서{i+1}] {c}" for i, c in enumerate(contexts))
    prompt = f"""당신은 RAG 시스템의 평가자입니다.
아래 '답변'을 문장 단위로 나누고, 각 문장이 '문서'들의 내용으로 뒷받침되는지 판정하세요.
문서에 근거가 있으면 뒷받침됨, 없으면 뒷받침 안 됨입니다.

문서:
{ctx}

답변:
{answer}

반드시 아래 JSON 형식으로만 답하세요:
{{"total": <전체 문장 수>, "supported": <뒷받침된 문장 수>}}"""
    data = _ask_json(prompt)
    total = data.get("total", 0)
    return data.get("supported", 0) / total if total else 0.0


def answer_relevancy(question: str, answer: str) -> float:
    """답변이 질문에 실제로 답하는 정도 (0~1)."""
    prompt = f"""당신은 RAG 시스템의 평가자입니다.
아래 '답변'이 '질문'에 얼마나 직접적으로 잘 답하는지 0.0~1.0 사이 점수로 평가하세요.
- 질문에 정확히 답하면 1.0에 가깝게
- 동문서답이거나 '정보를 찾을 수 없습니다'류면 0.0에 가깝게

질문: {question}
답변: {answer}

반드시 아래 JSON 형식으로만 답하세요:
{{"score": <0.0~1.0 사이 숫자>, "reason": "<짧은 이유>"}}"""
    data = _ask_json(prompt)
    return float(data.get("score", 0.0))


def context_precision(question: str, contexts: list[str]) -> float:
    """검색된 청크 중 질문에 관련 있는 것의 비율 (0~1)."""
    if not contexts:
        return 0.0
    relevant = 0
    for c in contexts:
        prompt = f"""아래 '문서 조각'이 '질문'에 답하는 데 관련이 있는지 판정하세요.

질문: {question}
문서 조각: {c}

반드시 아래 JSON 형식으로만 답하세요:
{{"relevant": <관련 있으면 1, 없으면 0>}}"""
        data = _ask_json(prompt)
        relevant += 1 if data.get("relevant", 0) == 1 else 0
    return relevant / len(contexts)
