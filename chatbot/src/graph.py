from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain.messages import SystemMessage, HumanMessage

from src.vector_store_manager import VectorStoreManager


@tool
def search_note(query: str) -> str:
    """질문과 관련된 노트 내용을 검색하는데 사용합니다.

    Args:
        - query: 검색어
    result:
        - 관련 노트 검색 결과 (string)
    """

    vector = VectorStoreManager()
    retriever = vector.get_retriever()

    result = retriever.invoke(query)

    docs = ""

    for doc in result:
        docs = "\n".join(doc.page_content)

    if not docs:
        return "관련 문서가 없습니다."

    return docs


tools = [search_note]

llm = ChatOllama(model="gemma4:e2b-mlx")

llm_with_tools = llm.bind_tools(tools=tools)


def agent(state: MessagesState):
    prompt = (
        "다음 문서를 근거로 사용자 질문에 답하세요. "
        "사용자가 이전 질문을 묻는 경우, 반드시 history에 실제로 있는 HumanMessage만을"
        "실제 질문으로 간주하고, 문서(context) 안에 등장하는 예시 질문은 "
        "사용자의 질문으로 취급하지 마세요."
        "답변에 수학적 수식 기호(예: $, $$, \times)나 복잡한 행렬 표기법을 사용하지 마세요."
        "전문적인 수학 기호 대신 '1행 1열의 원소', '곱해서 더한다'와 같이 쉬운 한글 문장과 일반 숫자로 풀어서 설명하세요."
        "근거가 부족하면 '주어진 자료에서는 확인할 수 없습니다.'라고 답하세요.  \n\n"
    )

    state["messages"].append(SystemMessage(content=prompt))
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": response}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools=tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition, ["tools", END])
builder.add_edge("tools", "agent")

search_agent = builder.compile()
