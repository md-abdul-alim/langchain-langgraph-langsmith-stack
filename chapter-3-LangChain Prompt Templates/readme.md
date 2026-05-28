# LangChain Prompt Templates

## What are Prompt Templates?

Prompt Templates in LangChain help create dynamic and reusable prompts for Large Language Models (LLMs). Instead of writing static prompts, developers can insert variables and structure prompts more efficiently.

---

# Main Prompt Template Types

## 1. String Prompt Template

Used for simple text-based prompts.

### Class

```python
PromptTemplate
```

### Example

```python
"Explain {topic} in simple words."
```

### Use Cases

* Basic LLM apps
* Text generation
* Dynamic variable insertion

---

## 2. Chat Prompt Template

Used for chat-based AI models like GPT or Gemini.

### Class

```python
ChatPromptTemplate
```

### Example

```python
[
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
]
```

### Use Cases

* Chatbots
* AI assistants
* Conversational systems

---

## 3. Few Shot Prompt Template

Used to provide examples before the actual user input.

### Classes

```python
FewShotPromptTemplate
FewShotChatMessagePromptTemplate
```

### Use Cases

* Teaching response patterns
* Better reasoning
* Structured outputs

---

## 4. Image Prompt Template

Used for multimodal or vision-based models.

### Class

```python
ImagePromptTemplate
```

### Use Cases

* Image generation
* Vision AI workflows
* Multimodal applications

---
