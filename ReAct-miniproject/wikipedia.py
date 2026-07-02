import logging
import wikipediaapi
import asyncio

from langchain_core.tools import tool

logger = logging.getLogger(__name__)

wiki_client = wikipediaapi.Wikipedia(
    user_agent="react-miniproject/1.0 vicki@ktb.com", language="ko"
)


@tool("search_wikipedia_tool")
async def search_wikipedia_tool(query: str) -> str:
    """위키백과에서 개념 정의, 역사적 사건, 인물 정보 등의 요약본을 검색합니다."""

    logger.info(f"[wiki] 검색 시작... (검색어: {query!r})")

    try:
        loop = asyncio.get_running_loop()
        page = await loop.run_in_executor(None, wiki_client.page, query)

        if not page.exists():
            logger.info(f"[wiki] '{query}' 문서 없음 -> 검색 실패")
            return f"'{query}'에 대한 위키백과 검색 결과가 없습니다."

        summary = await loop.run_in_executor(None, lambda: page.summary)

        logger.info(f"[wiki] 검색 완료: {page.title}")
        return f"위키백과 제목: {page.title}\n" f"내용: {summary[:1000]}"

    except Exception as e:
        logger.error(f"[wiki] 검색 중 오류: {e}")
        return f"위키백과 검색 중 오류가 발생했습니다: {e}"
