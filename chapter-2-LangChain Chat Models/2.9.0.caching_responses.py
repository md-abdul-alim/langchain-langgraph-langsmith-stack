"""
- How to
    - Identify the cache storage to use (memory, database)
    - Use LangChains `set_llm_cache` to set it as your response caching layer
    - If we use cache, for same input, the model will return the cached response instead of making a new API call
"""

import os
from load_env import load_env
from langchain_openai import ChatOpenAI
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache
from langchain_community.callbacks.manager import get_openai_callback

load_env()

model = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openai/gpt-oss-120b:free",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)

# Set up the cache
cache = InMemoryCache()
set_llm_cache(cache)

response = model.invoke("Who is the president of Bangladesh?")
print(response.content, "\n")

response2 = model.invoke("Who is the president of Bangladesh?")
print(response2.content, "\n")

