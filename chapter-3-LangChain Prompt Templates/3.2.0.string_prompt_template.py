from langchain_core.prompts import PromptTemplate

string_prompt1 = PromptTemplate(
    template="What year did {country} win the world cup?"
)

# recommended
string_prompt2 = PromptTemplate.from_template(
    "What year did {country} win the world cup?"
)

actual_prompt1 = string_prompt1.invoke({"country": "Argentina"})
print(actual_prompt1)
actual_prompt2 = string_prompt2.invoke({"country": "Argentina"})
print(actual_prompt2)