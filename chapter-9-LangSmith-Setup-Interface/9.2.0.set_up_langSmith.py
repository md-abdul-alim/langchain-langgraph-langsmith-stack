import os
from load_env import load_env
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_env() # LANGSMITH will auto connect by env data. no need extra code.

"""
LANGSMITH_API_KEY=lsv2_pt_2aba412905f946318135ae086a99
LANGSMITH_ENDPOINT=https://aws.api.smith.langchain.comm
LANGSMITH_PROJECT=TEST-PROJECT-1
LANGCHAIN_TRACING_V2=true
LANGSMITH_WORKSPACE_ID=1841ef02-8b32-4939-86dc
LANGCHAIN_CALLBACKS_BACKGROUND=False
"""
# No special LangSmith code needed - tracing is automatic
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")

llm = ChatOpenAI(
    model="qwen-plus",  # You can also use "qwen-max", "qwen-turbo", etc.
    api_key=os.getenv("ALIBABA_API_KEY"),
    base_url=os.getenv("ALIBABA_OPENAI_URL"),
)

chain = prompt | llm

result = chain.invoke({"topic": "developers"})
print(result.content)