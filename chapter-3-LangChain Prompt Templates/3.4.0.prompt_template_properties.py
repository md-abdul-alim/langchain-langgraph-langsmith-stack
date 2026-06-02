from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

prompt_template = PromptTemplate(
    template="Who is the {role} of {country}?",
    input_variables=["role", "country"],
    input_types={"role": str, "country": str},
    optional_variables=['gender'],
    validate_template=True,
)

print(prompt_template.template)
print(prompt_template.template_format)
print(prompt_template.input_variables)
print(prompt_template.input_types)
print(prompt_template.optional_variables)
print(prompt_template.validate_template, "\n")

chat_prompt_template = ChatPromptTemplate(
    messages=[
        ("system", "You are a helpful assistant that answers questions about the world cup."),
        ("human", "What year did {country} win the world cup?")
    ],
    input_variables=["country"],
    input_types={"country": str},
    optional_variables=['year'],
    validate_template=True,
)

print(chat_prompt_template.input_variables)