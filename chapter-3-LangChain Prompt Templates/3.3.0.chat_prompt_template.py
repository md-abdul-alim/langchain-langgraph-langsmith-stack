from langchain_core.prompts import ChatPromptTemplate

messages = [
    ("system", "You are a helpful assistant that answers questions about the world cup."),
    ("human", "What year did {country} win the world cup?"),
    ("ai", "{year}"),
    ("human", "What year did Brazil win the world cup?"),
    ("ai", "2002"),
]

chat_prompt_template = ChatPromptTemplate(messages)

chat_prompt = chat_prompt_template.invoke({"country": "Argentina", "year": "2022"})
print(chat_prompt)
print("-"*50)
print(chat_prompt.to_string())