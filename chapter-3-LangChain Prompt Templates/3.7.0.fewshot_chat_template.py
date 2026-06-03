"""
Chat Fewshot Template [Steps]
    - First, we create our example formatter with ChatPromptTemplate.from_messages() method and example list as with string prompts
    - We will the create an instance of our fewshot template, but this time using the FewShotChatMessagePromptTemplate and without the suffix, as the suffix is already defined in the example formatter.
    - We will then create a chat prompt template, and place the fewshot prompt before our user message to the model.
"""
import os
from load_env import load_env
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate, SystemMessagePromptTemplate

load_env()

model = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openai/gpt-oss-120b:free",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)

model_google = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    api_key=os.environ["GOOGLE_API_KEY"],
    temperature=0,
)

example_formatter = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template("{input}"),
    AIMessagePromptTemplate.from_template("{output}")
])

example_set = [
    {
        "input": "2 ribbit 2",
        "output": "4"
    },
    {
        "input": "5 ribbit 2",
        "output": "10"
    },
    {
        "input": "3 ribbit 3",
        "output": "9"
    },
]

few_shot_template = FewShotChatMessagePromptTemplate(
    example_prompt=example_formatter,
    examples=example_set
)

main_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a helpful assistant that can answer questions about basic math."),
    few_shot_template,
    HumanMessagePromptTemplate.from_template("{user_query}")
])

invoked_prompt = main_prompt.invoke({
    "user_query": "4 ribbit 5"
})

# print(invoked_prompt)
# print(invoked_prompt.to_string())


"""
response = model_google.invoke(invoked_prompt)
print(response.content[0].text)
"""

"""
formatted_prompt = main_prompt.format(user_query="6 ribbit 5")
response = model_google.invoke(formatted_prompt)
print(response.content)
"""

# LCEL = LangChain Expression Language

chain = main_prompt | model_google
response = chain.invoke({
    "user_query": "2 ribbit 7"
})
print(response.content)