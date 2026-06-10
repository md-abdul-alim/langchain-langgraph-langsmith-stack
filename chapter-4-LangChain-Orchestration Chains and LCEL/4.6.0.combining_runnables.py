import os
from load_env import load_env
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_env()

model = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openai/gpt-oss-120b:free",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)

prompt = ChatPromptTemplate.from_template("Write a short, concise sentence about {topic}.")

output_parser = StrOutputParser()

simple_chain = prompt | model | output_parser

result = simple_chain.invoke({"topic": "LangChain"})
print(result, "\n")

# Demo 2 - Chain to Runnable

combined_chain = simple_chain | (lambda chain_output: chain_output + " Oh wow, that's awesome!")

combined_chain_result = combined_chain.invoke({"topic": "LangChain"})
print('--- Combined Chain Result ---')
print(combined_chain_result, "\n")