"""
    Node are basically function. state is default argument

    def node_a(state: StateSchema, context_schema: Runtime[RuntimeContext]):
        value = state["key"]
        mysql_url = runtime.context.db_url

        return {"key": new_value, "key2": new_valu}

    builder = StateGraph(State)
    builder.add_node("my_node", send_email)
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime

class GraphState(TypedDict):
    input: str
    results: str

class ContextSchema(TypedDict):
    user_id: str


def plain_node(state: GraphState):
    print("Executing 'plain_node'...")

    return {"results": f"Hello, {state['input']}"}

def node_with_config(state: GraphState, config: RunnableConfig):
    print("Executing 'node_with_config'...")

    thread_id = config.get("configurable", {}).get("thread_id")
    print(f"--- Accessed thread_id from config: {thread_id}")

    return {"results": "Config Successful accessed"}

def node_with_runtime(state: GraphState, runtime: Runtime[ContextSchema]):
    print("Executing 'node_with_runtime'...")

    user_id = runtime.context['user_id']
    print(f"--- Accessed user_id from runtime: {user_id}")

builder = StateGraph(GraphState, context_schema=ContextSchema)

builder.add_node("plain_node", plain_node)
builder.add_node("node_with_config", node_with_config)
builder.add_node("node_with_runtime", node_with_runtime)

builder.add_edge(START, "plain_node")
builder.add_edge("plain_node", "node_with_config")
builder.add_edge("node_with_config", "node_with_runtime")
builder.add_edge("node_with_runtime", END)

graph = builder.compile()

# Run the Graph
initial_state = {
    "input": "Abdul Alim"
}

run_config = {
    "configurable": {
        "thread_id": "abc123"
    }
}

graph_context = {
    "user_id": "Optimus-103Prime"
}

final_state = graph.invoke(
    input=initial_state,
    config=run_config,
    context=graph_context
)

print("Final state: ")
print(final_state)
