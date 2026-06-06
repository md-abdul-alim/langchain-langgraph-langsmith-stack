import os
from load_env import load_env
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

load_env()

model = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openai/gpt-oss-120b:free",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)

# Demo 1: Lambda functions to runnables
runnable_multiply = RunnableLambda(lambda x: x * 2)

invoke_result = runnable_multiply.invoke(5)
print(invoke_result)  # Output: 10

batch_result = runnable_multiply.batch([1, 2, 3])
print(batch_result)  # Output: [2, 4, 6]

# Demo 2: Regular functions to runnables
def reverse_text_function(text: str) -> str:
    return text[::-1]

reverse_text_runnable = RunnableLambda(reverse_text_function)
result = reverse_text_runnable.invoke("Hello, World!")
print(result)  # Output: !dlroW ,olleH


text_batch_result = reverse_text_runnable.batch(["Hello", "World"])
print(text_batch_result)  # Output: ['olleH', 'dlroW']