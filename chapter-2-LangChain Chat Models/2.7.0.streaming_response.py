'''
    - Stream synchronously: wait till the chunks are received and processed before moving on to the next step (using stream()).
    - Stream asynchronously: allow the system to move to other tasks as you keep receiving chunks and processing them (using aiter_stream()).
    - Stream events: stream the intermediate events between the streaming process instead of prompts using (using aiter_events()).
'''

import os
from load_env import load_env
from langchain_google_genai import ChatGoogleGenerativeAI

load_env()

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    api_key=os.environ["GOOGLE_API_KEY"],
    temperature=0,
)

streamed_response = model.stream("Tell me about Rajshahi city in Bangladesh.")

# for chunk in streamed_response.stream():
#     print(chunk.content[0]['text'], end='', flush=True)

for chunk in streamed_response:
    print(chunk.content[0]['text'], end='', flush=True)