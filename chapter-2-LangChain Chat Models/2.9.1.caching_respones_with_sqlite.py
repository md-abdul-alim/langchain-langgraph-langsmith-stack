import os
from load_env import load_env
from langchain_openai import ChatOpenAI
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

load_env()

model = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openai/gpt-oss-120b:free",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)

# Set up the cache
cache = SQLiteCache(database_path="cache.db")
set_llm_cache(cache)

prompt = "Who is the president of Bangladesh?"
response = model.invoke(prompt)
print(response.content, "\n")

response2 = model.invoke(prompt)
print(response2.content, "\n")

