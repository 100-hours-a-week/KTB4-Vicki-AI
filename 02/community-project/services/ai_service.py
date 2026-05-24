import httpx

URL = "http://localhost:11434/v1/chat/completions"

class AIService:
    @staticmethod
    async def summarize(content: str) -> str:
        payload = {
            "model": "gemma4:e2b",
            "messages": [
                {
                    "role":"system",
                    "content": "너는 텍스트 요약 AI야. 핵심만 짧게 요약해줘"
                },
                {
                    "role":"user",
                    "content": content
                }
            ],
            "stream": False
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                URL,
                json=payload
            )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]