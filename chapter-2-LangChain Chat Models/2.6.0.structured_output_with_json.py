import os
from load_env import load_env
from pydantic import BaseModel, Field
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI

load_env()

model_google = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    api_key=os.environ["GOOGLE_API_KEY"],
    temperature=0,
)

"""
## Structured Output with JSON Schema. but for some unknow reason, it is not working with google gemini 3.5 flash, but it is working with openai gpt-4. So I am using openai gpt-4 for this example.
president_schema = {
    "name": "president_info_schema",
    "description": "Gets information about the president.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The full name of the president."
            },
            "country": {
                "type": "string",
                "description": "The country of the president."
            },
            "age": {
                "type": ["integer", "null"],
                "description": "The age of the president."
            }
        },
        "required": ["name", "country", ]
    }
}
"""

class PresidentInfo(BaseModel):
    name: str = Field(description="The full name of the president.")
    country: str = Field(description="The country of the president.")
    age: Optional[int] = Field(
        default=None,
        description="The age of the president."
    )

structured_llm = model_google.with_structured_output(PresidentInfo)
response = structured_llm.invoke("Who is president of the Bangladesh?")
print(response)