LangGraph components:
- Memory
    - Short term: current session of the ai agent is short term memory. Short term memory is meant for the current operation of the agent, think like RAM.
    - Long term: if the agent needs to reference memory that needs to be stored somewhere, then it has to call make use of long term memory. sementic information of object, user data, customer data. Long term memory is for any information that you need to persist, that agent always have to reference from time to time. think like hard drive.

- Human in the Loop
    - Human have the ability for of the agent pause operation, to pause operation so that a human being that is you or anyone using the AI agent can actually intervene in the current action.

- Streaming support
    - 

- How can we build agents in linggraph?
    - 1. Build agents using primitives, langgraph proved graph api and functional api.
        - One of the primitive ways for building agents in langgraph is called the graph API.
    - 2. Langgraph pre-build components



If you're preparing for a LangGraph interview, it's useful to explain the components from both a conceptual and practical perspective.

# What is LangGraph?

**LangGraph** is a framework from [LangGraph](https://langchain-ai.github.io/langgraph/?utm_source=chatgpt.com) for building **stateful, multi-step AI agents** using a graph-based workflow. Instead of a simple chain where steps run sequentially, LangGraph allows branching, loops, memory, and complex decision-making.

A concise interview definition:

> "LangGraph is a graph-based orchestration framework for LLM applications where nodes represent work units, edges represent transitions, and a shared state is passed through the graph, enabling agentic workflows, loops, and human-in-the-loop systems."

---

# Core LangGraph Components

## 1. State

State is the **shared data object** that flows through the graph.

Think of it as the application's memory during execution.

Example:

```python
class AgentState(TypedDict):
    question: str
    answer: str
    messages: list
```

### Interview Answer

> "State is the central data structure in LangGraph. Every node reads from and writes to the state, allowing information to persist across graph execution."

---

## 2. Nodes

Nodes are the **processing units** of the graph.

A node can:

* Call an LLM
* Execute a tool
* Query a database
* Perform validation
* Make decisions

Example:

```python
def generate_answer(state):
    response = llm.invoke(state["question"])
    return {"answer": response}
```

### Interview Answer

> "Nodes represent individual tasks in the workflow. Each node receives the current state, performs some operation, and returns updates to the state."

---

## 3. Edges

Edges define how execution moves between nodes.

### Normal Edge

```python
graph.add_edge("generate", "review")
```

Flow:

```text
Generate → Review
```

### Interview Answer

> "Edges define transitions between nodes and control the execution flow of the graph."

---

## 4. Conditional Edges

Conditional edges allow branching decisions.

Example:

```python
def route(state):
    if state["approved"]:
        return "publish"
    return "rewrite"
```

```python
graph.add_conditional_edges(
    "review",
    route
)
```

Flow:

```text
Review
 ├── Publish
 └── Rewrite
```

### Interview Answer

> "Conditional edges enable dynamic routing based on the current state, allowing the graph to make decisions at runtime."

---

## 5. START Node

Every graph has an entry point.

```python
from langgraph.graph import START
```

Example:

```python
graph.add_edge(START, "generate")
```

### Interview Answer

> "START is the predefined entry point where graph execution begins."

---

## 6. END Node

Marks completion of execution.

```python
from langgraph.graph import END
```

Example:

```python
graph.add_edge("publish", END)
```

### Interview Answer

> "END is the terminal node indicating that workflow execution has finished."

---

## 7. StateGraph

The graph builder used to define workflows.

Example:

```python
builder = StateGraph(AgentState)
```

### Interview Answer

> "StateGraph is the primary class used to define nodes, edges, state schema, and execution flow."

---

## 8. Compiled Graph

After defining the graph:

```python
graph = builder.compile()
```

Compilation converts the graph definition into an executable workflow.

### Interview Answer

> "The compiled graph is the runnable version of the workflow and can be invoked with input state."

---

## 9. Checkpointer (Persistence)

Allows saving and restoring state.

Examples:

* MemorySaver
* SQLite
* PostgreSQL

```python
graph = builder.compile(
    checkpointer=memory
)
```

### Interview Answer

> "Checkpointers provide persistence, enabling conversation memory, recovery, and long-running workflows."

---

## 10. Messages State

A common built-in state pattern for chat applications.

Example:

```python
from langgraph.graph import MessagesState
```

Contains:

```python
{
    "messages": [...]
}
```

### Interview Answer

> "MessagesState is a prebuilt state schema optimized for conversational agents, storing message history automatically."

---

## 11. Tools

Nodes often call tools.

Examples:

* Search APIs
* Databases
* Vector stores
* Calculators

Flow:

```text
User
  ↓
Agent
  ↓
Tool
  ↓
Agent
```

### Interview Answer

> "Tools allow agents to interact with external systems and retrieve information beyond the model's internal knowledge."

---

## 12. Human-in-the-Loop

LangGraph supports pausing execution for human approval.

Flow:

```text
Generate Report
      ↓
Human Review
      ↓
Approve/Reject
```

### Interview Answer

> "Human-in-the-loop functionality allows workflows to pause and wait for human feedback before continuing."

---

## 13. Memory

LangGraph supports:

### Short-Term Memory

Current workflow state.

### Long-Term Memory

Persistent storage across sessions.

### Interview Answer

> "LangGraph separates workflow state from persistent memory, enabling both session-level and long-term context retention."

---

# Typical LangGraph Architecture Interview Diagram

```text
           START
              │
              ▼
        User Input
              │
              ▼
         LLM Agent
              │
      ┌───────┴───────┐
      ▼               ▼
 Search Tool     Database
      │               │
      └───────┬───────┘
              ▼
         Decision Node
              │
              ▼
            END
```

---

# 30-Second Interview Answer

> "LangGraph is a graph-based framework for building stateful AI agents. The key components are State, which stores shared data; Nodes, which perform tasks; Edges and Conditional Edges, which control workflow transitions; START and END nodes for execution boundaries; StateGraph for defining workflows; Checkpointers for persistence; and tools, memory, and human-in-the-loop capabilities for building production-grade agent systems. Unlike traditional chains, LangGraph supports loops, branching, and complex agent orchestration."

This answer is usually sufficient for most LangGraph interview questions and demonstrates both conceptual understanding and practical usage.
