'''
    - Stream synchronously: wait till the chunks are received and processed before moving on to the next step (using stream()).
    - Stream asynchronously: allow the system to move to other tasks as you keep receiving chunks and processing them (using aiter_stream()).
    - Stream events: stream the intermediate events between the streaming process instead of prompts using (using aiter_events()).
'''

import os
import asyncio
from load_env import load_env
from langchain_google_genai import ChatGoogleGenerativeAI

load_env()

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)


async def process_stream():
    event_limit = 0
    prompt = "Describe padma river in Bangladesh."

    async for event_chunk in model.astream_events(prompt, version="v2"):
        # print(f"Event {event_limit}: {event_chunk.event}")
        print(f"Content: {event_chunk['data'].get('chunk', '')}\n")

        event_limit += 1
        if event_limit >= 5:
            print('...Event limit reached, stopping stream...')
            break

asyncio.run(process_stream())