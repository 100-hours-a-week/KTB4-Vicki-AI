import os
import httpx
import re
import logging

from dotenv import load_dotenv
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

load_dotenv()


@tool("search_naver_news")
async def search_naver_news(query: str) -> str:
    """네이버 뉴스에서 최신 시사, 트렌드, 사건 사고 정보를 검색합니다. 검색 결과는 기사 제목, 요약, 출처입니다."""

    logger.info(f"[naver] 검색 시작.... (검색어: {query!r})")

    try:
        url = f"https://openapi.naver.com/v1/search/news.json"

        headers = {
            "X-Naver-Client-Id": str(os.getenv("NAVER_CLIENT_ID")),
            "X-Naver-Client-Secret": str(os.getenv("NAVER_CLIENT_SECRET")),
        }

        params = {
            "query": query,
            "display": 5,
            "sort": "sim",
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=headers, params=params)

        response.raise_for_status()

        items = response.json().get("items", [])
        logger.info(f"[naver] 응답 status={response.status_code}, 결과 {len(items)}건")

        if not items:
            logger.info("[naver] 검색 결과 없음 -> 빈 결과 반환")
            return "검색 결과가 없습니다"

        results = []

        for item in items:
            title = item["title"]
            summary = item["description"]
            link = item["link"]

            clean_title = re.sub(r"<[^>]*>|&quot;|&amp;|&lt;|&gt;", "", title)
            clean_summary = re.sub(r"<[^>]*>|&quot;|&amp;|&lt;|&gt;", "", summary)

            results.append(
                f"기사 제목: {clean_title}\n요약: {clean_summary}\n출처: {link}"
            )

        logger.info(f"[naver] 검색 완료, {len(results)}건 반환")
        return "\n\n---\n\n".join(results)
    except Exception as e:
        logger.error(f"[naver]] 검색 중 오류: {e}")
        return f"네이버 뉴스 검색 중 오류가 발생했습니다: {e}"
