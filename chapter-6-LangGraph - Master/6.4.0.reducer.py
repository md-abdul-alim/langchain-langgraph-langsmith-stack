from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage
import os
from load_env import load_env
from langchain_openai import ChatOpenAI

load_env()

llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openai/gpt-oss-120b:free",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


def chat_node(state: AgentState) -> dict:
    conversation_history = state["messages"]
    response = llm.invoke(conversation_history)

    return {
        "messages": response
    }

graph = StateGraph(AgentState)

graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

agent = graph.compile()

message1 = HumanMessage(content="Hello, my name is Milon")

turn1_state = agent.invoke({
    "messages": message1
})

print('---Graph after first run---')
print(turn1_state)
print("-"*40)

# Turn 2
message2 = HumanMessage(content="What is your favorite color?")

turn2_state = agent.invoke({
    "messages": turn1_state["messages"] + [message2]
})

print('---Graph after second run---')
print(turn2_state)
print("-"*40)