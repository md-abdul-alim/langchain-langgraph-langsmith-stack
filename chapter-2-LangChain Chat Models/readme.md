
![alt text](2.1.1.How_LLM_Chat_Model_Takes_Input_and_Generates_Output.png)

![alt text](2.1.2.LLM_Chat_Processing_Architecture.png)

![alt text](2.2.0.message_roles_in_lang_chain_core.png)

🔹 Understanding Message Roles in LangChain Core

When building AI applications with LangChain, everything revolves around messages. But not all messages are the same.

✅ SystemMessage
Defines the AI's behavior and instructions.
Example: "You are a helpful Python tutor."

✅ HumanMessage
Represents the user's input.
Example: "What is Gradient Descent?"

✅ AIMessage
Represents the model's response.

✅ ToolMessage
Contains results returned from tools, APIs, databases, or external functions.

⚠️ RemoveMessage (Special Case)

Unlike the others, RemoveMessage is NOT a conversation role.

It is a state management operation used primarily in LangGraph to remove messages from the conversation history. This is useful for memory management, summarization, and reducing token usage in long-running agent workflows.

Think of it this way:

🧑 HumanMessage → User says something
🤖 AIMessage → Model responds
⚙️ ToolMessage → Tool returns data
📋 SystemMessage → Sets the rules
🗑️ RemoveMessage → Deletes old messages from state

Understanding these message types is essential when building production-grade agents and workflows with LangChain and LangGraph.