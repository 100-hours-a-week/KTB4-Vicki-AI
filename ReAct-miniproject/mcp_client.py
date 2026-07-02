import asyncio
import json
import os
import sys
import logging

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

SERVER_URL = f"http://127.0.0.1:{os.getenv('MCP_PORT', '8001')}/mcp"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    async with streamable_http_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            logger.info(f"Tools: {[t.name for t in tools.tools]}")

            if len(sys.argv) > 1:
                questions = [" ".join(sys.argv[1:])]
            else:
                print("질문을 입력하세요 (종료: exit 또는 Ctrl+D)")
                questions = iter(lambda: input(">").strip(), "exit")

            for question in questions:
                if not question:
                    continue
                args = {"question": question}

                result = await session.call_tool("check_fact", args)

                data = json.loads(result.content[0].text)
                print(data["answer"])


if __name__ == "__main__":
    asyncio.run(main())
