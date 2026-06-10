import os
from load_env import load_env
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_env()

model = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openrouter/owl-alpha",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)

prompt = ChatPromptTemplate.from_template("Write a short, concise sentence about {topic}.")

output_parser = StrOutputParser()

simple_chain = prompt | model | output_parser

result = simple_chain.invoke({"topic": "LangChain"})
print(result, "\n")
print("="*50 + '\n')

# Demo 2 - Chain to Runnable

combined_chain = simple_chain | (lambda chain_output: chain_output + " Oh wow, that's awesome!")

combined_chain_result = combined_chain.invoke({"topic": "LangChain"})
print('--- Combined Chain Result ---')
print(combined_chain_result, "\n")
print("="*50 + '\n')

# Demo 3 - Chain to Chain

fact_checking_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that fact-checks statements."),
    ("user", "Is it true that {statement}?")
])

checker_chain = fact_checking_prompt | model | output_parser

fact_checking_chain = { "statement": simple_chain } | checker_chain

dual_chain_result = fact_checking_chain.invoke({"topic": "LangChain is a programming language."})
print('--- Dual Chain Result ---')
print(dual_chain_result, "\n")
print("="*50 + '\n')