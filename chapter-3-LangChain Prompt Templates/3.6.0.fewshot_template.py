from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

example_formatter = PromptTemplate.from_template("Question: {question}\nAnswer: {answer}")

example_set = [
    {
        "question": "Tell me about the Bangladesh.",
        "answer": "Continent: South Asia. | Population: 170 million. | Capital: Dhaka. | Language: Bengali."
    },
    {
        "question": "Tell me about the Pakisthan.",
        "answer": "Continent: South Asia. | Population: 170 million. | Capital: Islamabad. | Language: Urdu."
    },
    {
        "question": "Tell me about the Iran.",
        "answer": "Continent: South Asia. | Population: 170 million. | Capital: Tehran. | Language: Persian."
    },
]

few_shot_prompt_template = FewShotPromptTemplate(
    example_prompt=example_formatter,
    examples=example_set,
    suffix="Question: {user_query}"
)

invoked_template = few_shot_prompt_template.invoke({
    "user_query": "Tell me about the Bangladesh."
})

# print(invoked_template)
print(invoked_template.text)