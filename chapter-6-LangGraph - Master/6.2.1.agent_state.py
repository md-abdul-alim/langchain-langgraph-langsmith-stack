from langgraph.graph import StateGraph, START, END
from typing import Annotated, List, TypedDict
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage


# Nodes
"""
- messages
- step_count
- private_date
"""

# 1. Using dict
def node_a(state):
    """A simple node that updates the state."""
    print("Executing Node A...")
    return {
        "messages": ["Step A Completed"],
        "step_count": 2
    }

def node_b(state):
    """A simple node that updates the state"""
    print("Executing Node B...")

    # Access and print some state information for demonstration
    if isinstance(state, dict):
        step_count = state["step_count"]
    else:
        step_count = state.step_count

    print(f"Current step count from state: {step_count}")

    return {
        "messages": ["Step B Completed"],
        "step_count": 1
    }

def build_and_run_graph(state_schema, initial_state):
    print(f"\n--- Building and Running graph with state schema: {state_schema.__name__ if hasattr(state_schema, "__name__") else "Dictionary"}")

    # Initiate the Graph
    graph = StateGraph(state_schema)

    # Add Nodes
    graph.add_node("node_a", node_a)
    graph.add_node("node_b", node_b)

    # Add Edges
    graph.add_edge(START, "node_a")
    graph.add_edge("node_a", "node_b")
    graph.add_edge("node_b", END)

    agent = graph.compile()

    final_state = agent.invoke(initial_state)

    print("\nFinal State")
    print(final_state)
    print("-"*40)

# Using a Plain Dictionary
def create_dict_state():
    return {
        "messages": [],
        "step_count": 0,
        "private_data": None
    }


build_and_run_graph(dict, create_dict_state())

# 2. Using TypedDict

def custom_add(current: int, new: int) -> int:
    return current + new


class TypedDictState(TypedDict):
    messages: Annotated[List[str], add_messages]
    step_count: Annotated[int, custom_add]
    private_data: str

build_and_run_graph(TypedDictState, {
    "messages": [],
    "step_count": 0,
    "private_data": ""
})
