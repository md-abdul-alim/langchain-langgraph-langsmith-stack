import os
from load_env import load_env
from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback

load_env()

model = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openai/gpt-oss-120b:free",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)

with get_openai_callback() as cb:
    response = model.invoke("What is the capital of Bangladesh?")
    response2 = model.invoke("Who is the president of Bangladesh?")

    print(cb, '\n')

print(f"Total tokens: {cb.total_tokens}")
print(f"Prompt tokens: {cb.prompt_tokens}")
print(f"Completion tokens: {cb.completion_tokens}")
print(f"Total cost (USD): {cb.total_cost}")

print(response.content)

'''
Tokens Used: 241
        Prompt Tokens: 148
                Prompt Tokens Cached: 128
        Completion Tokens: 93
                Reasoning Tokens: 24
Successful Requests: 2
Total Cost (USD): $0.0
'''