from langgraph.graph import StateGraph, START, END
from typing import Annotated, List, TypedDict
from langgraph.graph.message import add_messages

# 1. Define our state
class SimpleState(TypedDict):
    messages: Annotated[list, add_messages]

graph = StateGraph(SimpleState)

# 2. Create our nodes
def say_hello(state: SimpleState):
    print("Executing 'say_hello' node.")
    return {
        "messages": ['Hello', ]
    }

def say_world(state: SimpleState):
    print("Executing 'say_world' node.")
    return {
        "messages": ['World', ]
    }

graph.add_node("hello_node", say_hello)
graph.add_node("world_node", say_world)

# 3. Link nodes with edges
# Start -> hello_node -> world_node -> END
graph.add_edge(START, "hello_node")
graph.add_edge("hello_node", "world_node")
graph.add_edge("world_node", END)

# 4. Compile Graph
agent = graph.compile() # Runnable

# 5. Run Graph
initial_state = {
    "messages": []
}

final_state = agent.invoke(initial_state)

print("\n --- Final State ---")
print(final_state)
print("\n ---------------Graph Node visualization---------------")

print(agent.get_graph().draw_ascii())