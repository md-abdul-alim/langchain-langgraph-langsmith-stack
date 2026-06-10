import os
from load_env import load_env
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnableBranch

load_env()

# 1. LLM Setup
model = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openrouter/owl-alpha",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)

# Define Independent Runnables/Chains for Parallel Execution

# 2. Chain A: Generates a concise sentence about a given topic
sentence_prompt = ChatPromptTemplate.from_template(
    "Generate a concise sentence about the following topic: {topic}"
)

sentence_chain = sentence_prompt | model | StrOutputParser()

# 3. Chain B: Generates a few keywords related to the same topic
keywords_prompt = ChatPromptTemplate.from_template(
    "List 3-5 comma-separated keywords related to: {topic}. Do not include any extra text or intros."
)

keywords_chain = keywords_prompt | model | StrOutputParser()

# --- Combine Chains in Parallel ---
parallel_generation = RunnableParallel(
    sentence=sentence_chain,
    keywords=keywords_chain
)

# --- Define Conditional Logic (RunnableBranch) ---

# 5. Custom RunnableLambda for the condition check
def is_sentence_short(data: dict) -> bool:
    sentence = data.get("sentence", "")
    print(f"Checking sentence length: '{sentence}'")
    print(f"Sentence {sentence}: ({len(sentence)} characters)")
    is_short = len(sentence.split()) <= 50  # Check if the sentence has 50 words or fewer
    print(f"Is sentence short? {is_short}")
    return is_short

sentence_length_checker = RunnableLambda(is_sentence_short)

# 6. Branch 1: Elaborate if the sentence is short

elaborate_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("user", "Sentence: {sentence}\nKeywords: {keywords}\nElaboration:"),
    ]
)

elaborate_chain = elaborate_prompt | model | StrOutputParser()

# 7. Branch 2: Summarize if the sentence is long
summarize_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Summarize the following sentence concisely, using these keywords to guide the summary."),
        ("user", "Sentence: {sentence}\nKeywords: {keywords}\nSummary:"),
    ]
)
summarize_chain = summarize_prompt | model | StrOutputParser()

# 8. RunnableBranch: Directs flow based on the condition
conditional_branch = RunnableBranch(
    (sentence_length_checker, elaborate_chain),
    summarize_chain
)

# --- Assemble the Full Complex Chain ---

final_complex_chain = parallel_generation | conditional_branch

print('--- Visualizing the Complex Chain as ASCII Graph ---')
final_complex_chain.get_graph().print_ascii()