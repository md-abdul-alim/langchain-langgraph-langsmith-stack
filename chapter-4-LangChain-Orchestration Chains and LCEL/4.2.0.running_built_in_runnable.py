import os
from load_env import load_env
from langchain_openai import ChatOpenAI

load_env()

model = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openai/gpt-oss-120b:free",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)

# Demo 1 - Invoke
"""
invoked_prompt = "Where is the Eiffel Tower located?"

print("Invoked Prompt:", invoked_prompt, "\n")
response = model.invoke(invoked_prompt)
print(response.content, "\n")
"""

# Demo 2 - Batch Invoke
"""
batch_prompts = [
    "What is the capital of Bangladesh?",
    "What is the largest mammal?",
    "Who wrote 'To Kill a Mockingbird'?"
]

print("Batch Prompts\n")
responses = model.batch(batch_prompts)
for i, response in enumerate(responses):
    print(f"Response {i+1}: {response.content}")
"""

# Demo 3 - Stream
stream_prompt = "What are the benefits of using renewable energy?"
streamed_response = model.stream(stream_prompt)

for chunk in streamed_response:
    print(chunk.content, end="", flush=True)