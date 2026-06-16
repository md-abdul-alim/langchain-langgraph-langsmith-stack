"""
    Message Types:
        - HumanMessage
        - AIMessage
        - ToolMessage
        - SystemMessage

    messages: Annotated[List[str], operator.add]
    messages: Annotated[List[str], add_messages]

    MessagesState:
        - messages: Annotated[List[BaseMessage], add_messages]

    graph = StateGraph(MessagesState)

    class AgentState(MessagesState):
        step_count: int

    Message Format:
        - {"messages": [HumanMessage(content="")]}
        - {"messages": [{"role": "human", "content": ""}]}
"""
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class MyGraphState(MessagesState):
    turn_count: int

def user_node(state: MyGraphState) -> dict:
    print("Executing 'user_node'...")

    return {
        "messages": HumanMessage(content="What is the weather is like today?")
    }

def ai_node(state: MyGraphState):
    print("Executing 'ai_node'...")

    last_message = state["messages"][-1].content
    print(f"Human Prompt: {last_message}")

    response_content = f"I have received your message {last_message}, however i am not a fake response and can't respond.\n But atleast my coding is working."
    
    return {
        "messages": AIMessage(content=response_content)
    }

def counter_node(state: MyGraphState):
    print("Executing 'counter_node'...")

    return {
        "turn_count": state["turn_count"]
    }

graph = StateGraph(MyGraphState)

graph.add_node(user_node)
graph.add_node(ai_node)
graph.add_node(counter_node)

graph.add_edge(START, "user_node")
graph.add_edge("user_node", "ai_node")
graph.add_edge("ai_node", "counter_node")
graph.add_edge("counter_node", END)

agent = graph.compile()

initial_state = {
    "turn_count": 1,
}

final_state = agent.invoke(initial_state)

print("--- Final State ---")
print(final_state)

