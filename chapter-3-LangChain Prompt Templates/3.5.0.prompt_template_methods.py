"""
Template Methods
    - `invoke()`: Processes the template to generate a PromptValue
    - `format()`: Generates the string representation of the processed template
    - `format_prompt()`: Also produces a PromptValue but takes in keyword arguments
    - `batch()`: Processes a batch of prompts. Takes in a list of prompt parameters each for a specific prompt.
    - `pretty_print()`: Prints a pretty version of the prompt output
    - `save()`: Saves the prompt to a file
"""

from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("Who is the {role} of {country}?")

invoked_prompt = prompt.invoke({
    "role": "president",
    "country": "Bangladesh"
})
print(invoked_prompt, "\n")

format_prompt = prompt.format(
    role="president",
    country="Bangladesh"
)
print(format_prompt, "\n")

formatted_prompt = prompt.format_prompt(
    role="president",
    country="Bangladesh"
)
print(formatted_prompt, "\n")

batched_prompts = prompt.batch([
    {"role": "president", "country": "Bangladesh"},
    {"role": "prime minister", "country": "Canada"}
])
print(batched_prompts, "\n")

prompt.pretty_print()

prompt.save("prompt_template.yaml")