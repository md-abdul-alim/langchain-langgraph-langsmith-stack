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