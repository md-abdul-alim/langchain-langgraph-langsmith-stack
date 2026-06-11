import os
from load_env import load_env
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tracers.schemas import Run
from langchain_core.runnables import RunnableLambda
from typing import Any, Dict
import json

load_env()

# 1. LLM Setup
model = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openrouter/owl-alpha",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)

def failing_function(input_dict: Dict[str, Any]) -> str:
    topic = input_dict.get("topic", "unknown")
    lower_topic = topic.lower()

    if 'error' in lower_topic:
        raise ValueError(f"Intentional error triggered by topic: {topic}")
    elif 'network' in lower_topic:
        raise ConnectionError(f"Simulated netword connection failure.")
    elif 'json' in lower_topic:
        bad_json = '{"incomplete": json}'
        return json.loads(bad_json)
    else:
        return f"Processing topic: {topic}"
    
error_runnable = RunnableLambda(failing_function)

def my_listener_on_error(run: Run):
    print(f"Run ID {run.id}")
    print(f"Error name: {run.name}")
    print(f"Start time: {run.start_time}")
    print(f"End time: {run.end_time}")
    print("Input: {run.inputs}")
    print("Output: {run.outputs}")

    print("--- Error Details ---")
    print(run.error)

error_runnable_with_listeners = error_runnable.with_listeners(on_error=my_listener_on_error)

print("--- Demo: Running Error Scenario ---")

try:
    result = error_runnable_with_listeners.invoke({
        'topic': "error somewhere here"
    })

    print("Result: {result}")
except Exception as e:
    print("An error occurred")