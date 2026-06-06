import asyncio
from langchain_core.runnables import RunnableLambda


# Demo 1: Lambda functions to runnables
runnable_multiply = RunnableLambda(lambda x: x * 2)

invoke_result = runnable_multiply.invoke(5)
print(invoke_result)  # Output: 10

batch_result = runnable_multiply.batch([1, 2, 3])
print(batch_result, "\n")  # Output: [2, 4, 6]

# Demo 2: Regular functions to runnables
def reverse_text_function(text: str) -> str:
    return text[::-1]

reverse_text_runnable = RunnableLambda(reverse_text_function)
result = reverse_text_runnable.invoke("Hello, World!")
print(result, "\n")  # Output: !dlroW ,olleH


text_batch_result = reverse_text_runnable.batch(["Hello", "World"])
print(text_batch_result, "\n")  # Output: ['olleH', 'dlroW']

# Demo 3: Async functions to runnables
async def async_reverse_text_function(text: str) -> str:
    aresult = await reverse_text_runnable.ainvoke(text)
    print(f"Async result: {aresult}")  # Output: Async result: !dlroW ,olleH

asyncio.run(async_reverse_text_function("Hello, World!"))

batch_async_inputs = ["Hello", "World"]

async def anync_batch_reverse_text():
    batch_async_result = await reverse_text_runnable.abatch(batch_async_inputs)
    print(f"Async batch result: {batch_async_result}")  # Output: Async batch result: ['olleH', 'dlroW']


asyncio.run(anync_batch_reverse_text())