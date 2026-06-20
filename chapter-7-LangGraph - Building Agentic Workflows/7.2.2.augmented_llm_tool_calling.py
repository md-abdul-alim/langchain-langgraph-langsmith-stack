import os
from load_env import load_env
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
load_env()

@tool
def get_weather(city: str) -> str:
    """Get the weather for a city"""

    weather_data = {
        "New York": "Sunny, 72 F",
        "Rajshahi": "Cloudy, 90F",
        "Dhaka": "Rainy, 20 C"
    }

    return weather_data.get(city, "Weather data not available")

@tool
def calculate_tip(bill_amount: float, tip_percentage: float) -> float:
    """Calculate tip amount based on bill and percentage"""

    return round(bill_amount * (tip_percentage/100), 2)

llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openai/gpt-oss-120b:free",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)

llm_with_tools = llm.bind_tools([
    get_weather,
    calculate_tip
])

weather_prompt = "What's the weather in Dhaka?"
tip_amount = "Calculate a 20% tip on a $70 bill"

# response = llm_with_tools.invoke(weather_prompt)
response = llm_with_tools.invoke(tip_amount)

tool_calls = response.tool_calls
# print(tool_calls)

for tool_call in tool_calls:
    if tool_call['name'] == 'get_weather':
        result = get_weather.invoke(tool_call["args"])
    elif tool_call['name'] == 'calculate_tip':
        result = calculate_tip.invoke(tool_call["args"])
    else:
        result = "No tool found"

print('Result: ', result)