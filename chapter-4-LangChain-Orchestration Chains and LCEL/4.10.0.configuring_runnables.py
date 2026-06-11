import os
from load_env import load_env
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig, ConfigurableField
from langchain_core.tracers.schemas import Run

load_env()

model = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openrouter/owl-alpha",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
).configurable_fields(
    max_tokens=ConfigurableField(
        id='llm_token_cap',
        name='LLM Maximum Response Tokens',
        description='Maximum number of tokens to be used for response'
    ),
)

prompt = ChatPromptTemplate.from_template("Give simple fact about {topic}")
parser = StrOutputParser()

base_chain = prompt | model | parser

print('--- Invoking with default token limit ---')
result_default = base_chain.invoke({'topic': "The Moon"})
print(f'Fact about the moon (Max Tokens=default): {result_default}')

print('--- Invoking with a low token limit ---')
low_tokens_config = RunnableConfig(
    configurable={
        'llm_token_cap': 10
    }
)

result_low_tokens = base_chain.invoke(
    {"topic": "The Moon"},
    config=low_tokens_config
)

print(f"Fact about the moon (Max Tokens=10): {result_low_tokens}", '\n\n')
print('==='*10)
def my_listener_on_start(run: Run): 
    """Logs when the chain starts, accessing data from the Run object"""
    print(f"Listener START for '{run.name}' (Run ID: {run.id})", '\n')
    print(f"Inputs: {run.inputs}", '\n')
    print(f"Parent Run ID: {run.parent_run_id}", '\n')
    print(f'Tags: {run.tags}, Metadata: {run.extra.get("metadata")}', '\n')

chain_with_listeners = base_chain.with_listeners(
    on_start=my_listener_on_start
)

my_runnable_configuration = RunnableConfig(
    run_name="Configuration Demo",
    tags=['single_run_tag', 'demo_invoke'],
    metadata={
        'user_id': "234234sfsf",
        'source': 'manual_test',
        'input_topic_type': 'history'
    }
)

print('--- Demo 1: Per-Invocation Configuration ---')

per_invoke_result = chain_with_listeners.invoke(
    {
        "topic": "The Mughal Empire"
    },
    config=my_runnable_configuration
)

print(f"Result: {per_invoke_result}")

print('\n\n--- Demo 2: Persistent Configuration ---')

my_persistent_configuration = RunnableConfig(
    run_name="Persistent Config Demo",
    tags=['persistent_tag', 'demo2_invoke'],
    metadata={
        'user_id': "23sdfsfssfs",
        'source': 'manual_test',
        'input_topic_type': 'animals'
    }
)

persistent_chain = chain_with_listeners.with_config(my_persistent_configuration)

persistent_result = persistent_chain.invoke(
    {
        "topic": "Royal Bengal Tiger"
    }
)

print(f"Result: {persistent_result}")