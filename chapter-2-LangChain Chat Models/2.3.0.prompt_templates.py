import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

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

prompt1 = PromptTemplate(template="What is the capital of Bangladesh?")

# Recommended way to create a prompt template
prompt2 = PromptTemplate.from_template("Who is the president of {country}?")

# print(prompt1.invoke({}))
# print(prompt2.format(country="Bangladesh"))
# print(prompt2.invoke({"country": "Bangladesh"}))


## Fill the template first, then pass the resulting string to invoke
# filled_prompt = prompt2.format(country="Bangladesh")
filled_prompt = prompt2.invoke({
    "country": "Bangladesh"
})

response = model_google.invoke(filled_prompt)
print(response.content[0]['text'])