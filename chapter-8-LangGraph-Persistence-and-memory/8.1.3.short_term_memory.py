import os
from load_env import load_env
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from typing import TypedDict, List, Annotated, Literal
from operator import add
from langgraph.types import Send
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage

load_env()

llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openai/gpt-oss-120b:free",
    temperature=0.7,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)

def chatbot(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {
        "messages": [response]
    }

builder = StateGraph(MessagesState)

builder.add_node(chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

checkpointer = MemorySaver()

graph = builder.compile(checkpointer=checkpointer) # this is where STM works

config = {
    "configurable": {
        "thread_id": "chat_session_1"
    }
}

# Turn 1
message_1 = "Hi! my name is Milon, I am an AI Engineer"

input_1 = {
    "messages": [HumanMessage(content=message_1)]
}

result_1 = graph.invoke(input_1, config=config) # also need to add this config

print(f"User: {message_1}")
print(f"AI: {result_1['messages'][-1].content}")

# Turn 2
message_2 = "What's is my name?"

input_2 = {
    "messages": [HumanMessage(content=message_2)]
}

result_2 = graph.invoke(input_2, config=config)

print(f"User: {message_2}")
print(f"AI: {result_2['messages'][-1].content}")

