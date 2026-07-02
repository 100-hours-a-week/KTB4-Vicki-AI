import logging

from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from wikipedia import search_wikipedia_tool
from naver_news import search_naver_news

logger = logging.getLogger()

tools = [search_wikipedia_tool, search_naver_news]

llm = ChatOllama(model="gemma4:e2b-mlx")

llm_with_tools = llm.bind_tools(tools)


class AIResponse(BaseModel):
    question: str = Field(description="사용자 질문 원본")
    wiki_docs: list[str] = Field(
        description="위키백과 검색 결과. 페이지 제목, 본문 요약 포함"
    )
    news_docs: list[str] = Field(
        description="네이버 뉴스 검색 결과. 기사 제목, 요약, 원본 링크 포함"
    )
    response: str = Field(
        description="사용자 질문 팩트 체크 결과. 신뢰도, 근거와 출처 포함"
    )


llm.with_structured_output(AIResponse)


def agent(state: MessagesState):
    logger.info("agent 작업 시작 ")
    prompt = SystemMessage(
        content="당신은 사용자의 말에 대한 팩트체크를 하는 agent입니다."
        "사용자 질문이 들어오면 사실을 확인하기 위해 검색해야 할 키워드 목록을 뽑습니다."
        "그 후 관련 키워드들을 네이버나 위키백과에 검색하여 근거가 될 내용을 찾아봅니다."
        "근거가 될 내용을 기준으로 팩트 확룔을 계산합니다."
        "예를 들어 사용자의 질문이 '파이썬은 컴파일 언어다.' 라면"
        "키워드인 '파이썬', '컴파일 언어'를 위키백과에 검색해봅니다. "
        "검색 결과를 바탕으로 사용자의 말의 팩트인지 확률을 계산합니다."
        "응답의 구조는 "
        "[사용자 질문] '파이썬은 컴파일 언어다.'\n"
        "[팩트 확률]: 0 (%) \n"
        "[근거] \n"
        "   1. 파이썬은 인터프리터 언어다. (출처) 위키백과 '파이썬' 페이지\n"
        " 형식으로 합니다."
        "그리고 사용자의 질문이 '삼성전자는 배우 엔터테이먼트 회사다'일 경우"
        "키워드인 '삼성전자' 관련 기사를 네이버에 검색해봅니다."
        "[사용자 질문] 삼성전자는 배우 엔터테이먼트 회사다\n"
        "[팩트 확률] 0 (%)"
        "[근거] \n"
        "   1. 삼성전자는 반도체 회사입니다. (출처) 삼성전자 기사"
        "중요: 기업, 인물의 최근 행보, 시사, 사건 사고 등 최신성이 중요한 주제는 "
        "위키백과 검색 결과만으로 판단하지 말고 반드시 search_naver_news도 함께 호출하여 "
        "두 출처를 모두 근거로 사용합니다. "
        "위키백과에서 이미 답을 찾은 것 같아도 최신 뉴스 검증을 생략하지 않습니다. "
        "사용자 질문(HumanMessage)는 변경하지 않습니다."
    )
    state["messages"].append(prompt)
    response = llm_with_tools.invoke(state["messages"])

    if response.tool_calls:
        for call in response.tool_calls:
            logger.info(f"[agent] 도구 호출 결정: {call['name']}({call['args']})")
    else:
        logger.info(f"[agent] 최종 응답 (도구 호출 없음): {response.content}")

    return {"messages": [response]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools=tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition, ["tools", END])
builder.add_edge("tools", "agent")

factcheck_agent = builder.compile()
