import os
from load_env import load_env
from langchain_google_genai import ChatGoogleGenerativeAI

load_env()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ["GOOGLE_API_KEY"],
)

response = model.invoke("What is the capital of Bangladesh?")

print(response.usage_metadata)  # Additional metadata about the API call and token usage
'''
{'input_tokens': 8, 'output_tokens': 30, 'total_tokens': 38, 'input_token_details': {'cache_read': 0}, 'output_token_d
etails': {'reasoning': 21}}
'''