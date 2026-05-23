import getpass
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI


# model_anthropic = ChatAnthropic(model="claude-2", temperature=0.9, api_key="sk-ant-")
# model_openai = ChatOpenAI(model="gpt-4o", temperature=0.9, api_key="sk-proj-")


if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

model_google = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.environ["GOOGLE_API_KEY"],
)


# 1 prompt 1 response
"""
# response = model_google.invoke("What is the capital of Bangladesh?") # 1 prompt 1 response
# print(response.content)
"""

