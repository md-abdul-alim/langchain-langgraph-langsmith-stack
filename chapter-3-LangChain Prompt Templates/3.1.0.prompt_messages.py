from langchain_core.messages import HumanMessage, SystemMessage

user_message = HumanMessage(content="Always reply in {language} language.")
system_message = SystemMessage(content="You are a helpful assistant.")

prompt1 = [
    user_message,
    system_message
]
print(prompt1)

prompt2 = [
    {"role": "user", "content": "Always reply in {language} language."},
    {"role": "system", "content": "You are a helpful assistant."}
]
print(prompt2)

prompt3 = [
    ("user", "Always reply in {language} language."),
    ("system", "You are a helpful assistant.")
]
print(prompt3)