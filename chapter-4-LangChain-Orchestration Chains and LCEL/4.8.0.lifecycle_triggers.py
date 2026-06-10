import os
from load_env import load_env
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnableBranch
from langchain_core.tracers.schemas import Run

load_env()

# 1. LLM Setup
model = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openrouter/owl-alpha",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)

prompt = ChatPromptTemplate.from_template("Give me a very short, simple fact about {topic}")

fact_chain = prompt | model | StrOutputParser()

def my_listener_on_start(run: Run): 
    """Logs when the chain starts, accessing data from the Run object"""
    print(f"Listener START for '{run.name}' (Run ID: {run.id})")
    print(f"Inputs: {run.inputs}")
    print(f"Parent Run ID: {run.parent_run_id}")
    print(f'Tags: {run.tags}, Metadata: {run.extra.get("metadata")}')


def my_listener_on_end(run: Run):
    """Logs when the chain ends, accessing data from the Run object"""
    print(f"Listener END for '{run.name}' (Run ID: {run.id})")
    print(f"Output Type: {type(run.outputs).__name__}, Output Values: {run.outputs}")
    print(f"Parent Run ID: {run.parent_run_id}")
    print(f'Tags: {run.tags}, Metadata: {run.extra.get("metadata")}')

fact_chain_with_listeners = fact_chain.with_listeners(
    on_start=my_listener_on_start,
    on_end=my_listener_on_end
)

result = fact_chain_with_listeners.invoke({
    "topic": "The Eiffel Tower",
})

print(f"Final Result {result}")
print('-'*20)