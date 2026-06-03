"""
Chat Fewshot Template [Steps]
    - First, we create our example formatter with ChatPromptTemplate.from_messages() method and example list as with string prompts
    - We will the create an instance of our fewshot template, but this time using the FewShotChatMessagePromptTemplate and without the suffix, as the suffix is already defined in the example formatter.
    - We will then create a chat prompt template, and place the fewshot prompt before our user message to the model.
"""
from langchain_core.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate

example_formatter = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
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
    ("system", "You are a helpful assistant that can answer questions about basic math."),
    few_shot_template,
    ("human", "{user_query}")
])

invoked_prompt = main_prompt.invoke({
    "user_query": "4 ribbit 5"
})

# print(invoked_prompt)
print(invoked_prompt.to_string())