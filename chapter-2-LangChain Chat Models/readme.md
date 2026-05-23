
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


# Prompt Templates
![alt text](2.3.1.prompt_templates.png)
## Prompt Templates in LangChain Core

Prompt templates are one of the most important concepts in LangChain. They help create dynamic prompts by inserting variables, conversation history, examples, and retrieved context before sending requests to an LLM.

---

## Why Use Prompt Templates?

Instead of hardcoding prompts:

```python
prompt = "Explain Gradient Descent"
```

You can create reusable templates:

```python
prompt = "Explain {topic}"
```

And inject values dynamically:

```python
topic = "Gradient Descent"
```

Result:

```text
Explain Gradient Descent
```

---

## 1. PromptTemplate

Used for simple text prompts.

## Example

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="Explain {topic} in simple terms.",
    input_variables=["topic"]
)

result = prompt.invoke({
    "topic": "Gradient Descent"
})

print(result.text)
```

Output:

```text
Explain Gradient Descent in simple terms.
```

---

## 2. ChatPromptTemplate

Used for chat models such as GPT, Claude, Gemini, and others.

## Example

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI tutor."
    ),
    (
        "human",
        "{question}"
    )
])

messages = prompt.invoke({
    "question": "What is LangGraph?"
})

print(messages)
```

Generated Messages:

```python
[
    SystemMessage(
        content="You are a helpful AI tutor."
    ),
    HumanMessage(
        content="What is LangGraph?"
    )
]
```

---

## 3. MessagesPlaceholder

Used to inject chat history dynamically.

## Example

```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant."
    ),
    MessagesPlaceholder("history"),
    (
        "human",
        "{question}"
    )
])

messages = prompt.invoke({
    "history": [
        HumanMessage(content="Hello"),
        AIMessage(content="Hi! How can I help?")
    ],
    "question": "What is LangGraph?"
})
```

Result:

```python
[
    SystemMessage(...),
    HumanMessage("Hello"),
    AIMessage("Hi! How can I help?"),
    HumanMessage("What is LangGraph?")
]
```

---

## 4. FewShotPromptTemplate

Used when you want to teach the model through examples.

## Example

```python
from langchain_core.prompts import (
    PromptTemplate,
    FewShotPromptTemplate
)

examples = [
    {
        "input": "2+2",
        "output": "4"
    },
    {
        "input": "3+3",
        "output": "6"
    }
]

example_prompt = PromptTemplate(
    template="Input: {input}\nOutput: {output}",
    input_variables=["input", "output"]
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Input: {input}",
    input_variables=["input"]
)

result = few_shot_prompt.invoke({
    "input": "5+5"
})
```

Generated Prompt:

```text
Input: 2+2
Output: 4

Input: 3+3
Output: 6

Input: 5+5
```

---

## 5. FewShotChatMessagePromptTemplate

Used for chat-based few-shot prompting.

## Example

```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate
)
```

Commonly used in AI agents and advanced chatbot workflows.

---

# Common Production Prompt Structure

Most real-world AI applications follow this structure:

```text
System Instructions
│
├── Role Definition
├── Rules
├── Constraints
├── Output Format
│
Conversation History
│
Retrieved Context (RAG)
│
User Question
│
Final Response
```

Example:

```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a senior Python tutor.

        Rules:
        - Explain simply
        - Use examples
        - Use markdown
        """
    ),

    MessagesPlaceholder("history"),

    (
        "human",
        """
        Context:
        {context}

        Question:
        {question}
        """
    )
])
```

---

## Most Commonly Used Templates

| Template                         | Purpose                    |
| -------------------------------- | -------------------------- |
| PromptTemplate                   | Simple text prompts        |
| ChatPromptTemplate               | Chat applications          |
| MessagesPlaceholder              | Conversation history       |
| FewShotPromptTemplate            | Example-based learning     |
| FewShotChatMessagePromptTemplate | Example-based chat prompts |

---


```python
ChatPromptTemplate
MessagesPlaceholder
```

These two classes form the foundation of most LangChain applications.
