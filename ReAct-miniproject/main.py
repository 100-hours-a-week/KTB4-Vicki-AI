import os
import asyncio
import logging

from mcp.server.fastmcp import FastMCP
from factcheck import factcheck_agent

mcp = FastMCP("factchecker", port=int(os.getenv("MCP_PORT", "8001")))

logging.basicConfig(filename="factcheck.log", level=logging.INFO)
logger = logging.getLogger(__name__)


@mcp.tool()
async def check_fact(question: str):
    logger.info(f"Started with quetion: {question}")

    response = await factcheck_agent.ainvoke({"messages": [("user", question)]})

    final_answer = response["messages"][-1].content
    logger.info(f"최종 답변:  {final_answer}")
    return {"answer": final_answer}


if __name__ == "__main__":
    # asyncio.run(main())
    mcp.run(transport="streamable-http")
