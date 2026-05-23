import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

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

systemInstruction = SystemMessage(content="Reply every prompt in bangla Language.")
userMessage = HumanMessage(content="what is the independence day of Bangladesh?")

response = model_google.invoke([
    systemInstruction,
    userMessage
])

print(response.content[0]['text'])