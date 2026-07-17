# langchain-langgraph-langsmith-stack

For openrouter free model visit: https://openrouter.ai/collections/free-models
For openrouter api key: https://openrouter.ai/workspaces/default/keys

LCEL = LangChain Expression Language

Doc: https://www.promptingguide.ai/introduction

different between invoke() vs ainvoke()

we can not steam an llm response which return structured response.

`
https://gofastmcp.com/
https://modelcontextprotocol.io/
https://mcp.so/
`

What is middleware? Need to learn middleware use in agent.
differece between ChatOpenAI vs init_chat_model

https://www.langchain.com/blog/what-is-an-agent


https://files.cdn.thinkific.com/file_uploads/967498/attachments/ecd/3cc/6d3/LangChain_Academy_-_Introduction_to_LangGraph_-_Motivation.pdf

What is ReAct?
    By invoking a model, we normally call a tool with return ToolMessage by router.
    If we simple pass that ToolMessage back to the model?
    We can let the model either call another tool or return a response.
    This is a ReAct pattern.

        - act -> let the model decide to call a tool or return a response.
        - observe -> pass the tool output back to the model
        - repeat -> let the model decide to call a tool or return a response.


How many way we can define state?
    - 3 ways:
        - TypedDict
        - dataclass
        - pydantic


What is the use of reducer? what problem is solve?
    - 

Difference between InMemorySaver, MemorySaver?
    -

# What is memory?
    - Memory is a cognitive function that allows people to store, retrieve, and use information to understand their present and future.

# Short Term VS Long Term Memory

|  | Short-Term | Long-Term |
|----------|----------|----------|
| Scope    | Within session (thread)     | Across session (thread)     |
| Example use-case    | Persist conversational history, allow interruptions in a chat (if user is idle or to allow human-in-the-loop)   | Remember information about a specific user across all chat sessions.   |
| LangGraph usage    | Checkpointer     | Store     |
|

# What is the type of memory?
|       | Semantic | Episodic | Procedural |
|-------|----------|----------|----------|
|       | Facts    | Memories     | Instructions     |
| Human  | Bike model I have    | Bike rides I took     | Motor skills     |
| Agent  | Facts about a user    | Past agent actions    | Agent's system prompt |
|

# When do you want to update memories?
    - In the Hot-path
    - In the Backgroun
|           |             Type              |       Pro             |          Con           |
|-----------|-------------------------------|-----------------------|------------------------|
| Hot Path  |   During runtime (ChatGPT)    | Real-time updates with transparency for user|     Can affect UX/Latency and degrade performance   |
| Background          | As a separate process   | Lower risk of UX / Performance degradation |  Frequency of memory writing needs to be tuned   |
|

# What is context window (Tokens)

# Difference between different vector database? when to use which database?
  