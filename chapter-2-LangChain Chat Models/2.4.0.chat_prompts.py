import os
from load_env import load_env
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


load_env()

model_google = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.environ["GOOGLE_API_KEY"],
)


prompts = [
    ('system', 'Reply every prompt in {language} language.'),
    ('user', 'why {city} is famous?')
]

chat_prompt = ChatPromptTemplate(prompts)
formatted_prompt = chat_prompt.invoke({
    'language': 'Bangla', 
    'city': 'Rajshahi'
})

# print(formatted_prompt)

response = model_google.invoke(formatted_prompt)
print(response.content[0]['text'])