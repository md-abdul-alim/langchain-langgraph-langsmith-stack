"""
RetryPplicy(
    max_attempts = 5 # int
    initial_interval = 2 # float
    backoff_factor = 1.5 # float
    max_interval = 128 # float
    jitter = True # bool
    retry_on = (Exception, TimeoutError, ConnectionError, RateLimitError, sqlite3.OperationalError)
)
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy
import random

class WeatherState(TypedDict):
    city: str
    temperature: float
    conditions: str

class APIError(Exception):
    """Simulated error"""
    pass


def fetch_weather(state: WeatherState):
    city = state['city']

    """Simulate request"""
    if random.random() < 0.7:
        print(f"X - API call failed for {city}")
        raise APIError(f"Weather API timeout or {city}")
    
    print(f"Successfully fetched weather for {city}")

    temp = round(random.uniform(15, 30), 1)
    conditions = random.choice(["Sunny", "Cloudy", "Rainy", "Partially Cloudy"])

    return {
        "temperature": temp,
        "conditions": conditions
    }

def format_result(state: WeatherState):
    print(f"\n Weather Report for {state['city']}")
    print(f"Temperature: {state['temperature']} degrees")
    print(f"Conditions: {state['conditions']}")

    return state

builder = StateGraph(WeatherState)

builder.add_node(
    "fetch_weather",
    fetch_weather,
    retry_policy=RetryPolicy(
        max_attempts=5,
        initial_interval=1,
        backoff_factor=2.0,
        max_interval=10.0,
        jitter=True,
        retry_on=APIError
    )
)
builder.add_node(format_result)

builder.add_edge(START, "fetch_weather")
builder.add_edge("fetch_weather", "format_result")
builder.add_edge("format_result", END)

graph = builder.compile()

"""Test The Graph"""

try:
    result = graph.invoke({
        "city": "Rajshahi",
        "temperature": 0.0,
        "conditions": ""
    })

    print(f"\n Final result: {result}")
except Exception as e:
    print(f"\n All retry attempts exhausted: {e}")