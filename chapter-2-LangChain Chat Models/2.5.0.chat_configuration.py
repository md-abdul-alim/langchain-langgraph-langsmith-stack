import os
from load_env import load_env
from langchain_google_genai import ChatGoogleGenerativeAI


load_env()

model_google = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    api_key=os.environ["GOOGLE_API_KEY"],
    max_tokens=100,
)

response = model_google.invoke("Explain quantum computing?")
print(response.content[0]['text'])