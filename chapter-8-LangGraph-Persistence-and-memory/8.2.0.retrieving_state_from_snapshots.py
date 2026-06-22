import os
from load_env import load_env
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END, MessagesState
from typing import TypedDict, List, Annotated, Literal
from operator import add
from langgraph.types import Send
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage

load_env()

# Don't use gpt-4 or lower, they don't support JSON mode or JSON schemas for structured outputs
# llm = ChatOpenAI(
#     openai_api_base="https://openrouter.ai/api/v1",
#     model_name="openai/gpt-oss-120b:free",
#     temperature=0.7,
#     openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
# )
llm = ChatOpenAI(
    model="qwen-plus",  # You can also use "qwen-plus", "qwen-max", "qwen-turbo", etc.
    api_key=os.getenv("ALIBABA_API_KEY"),
    base_url=os.getenv("ALIBABA_OPENAI_URL"),
)
# Define state
class DocumentState(TypedDict):
    """State for document processing workflow"""
    document_title: str
    document_content: str
    processing_stage: str
    quality_score: int
    issues_found: list[str]
    revisions_made: list[str]
    approved: bool

# Structured output for analysis
class QualityAnalysis(BaseModel):
    """Quality analysis result"""
    score: int = Field(description="Quality score 1-10", ge=1, le=10)
    issues: list[str] = Field(description="List of issues found")
    recommendation: Literal["approve", "revise", "reject"]

# Node 1: Intake
def intake_document(state: DocumentState):
    """Receive and log document"""
    print(f"\n📄 INTAKE: Processing '{state['document_title']}'")
    print(f"   Content length: {len(state['document_content'])} characters")
    
    return {
        "processing_stage": "intake_complete"
    }


# Node 2: Initial Analysis
def analyze_quality(state: DocumentState):
    """Analyze document quality"""
    print(f"\n🔍 ANALYSIS: Evaluating quality...")
    
    analyzer_llm = llm.with_structured_output(QualityAnalysis)
    
    prompt = f"""Analyze this document for quality:

        Title: {state['document_title']}
        Content: {state['document_content']}

        Evaluate for:
        - Clarity and structure
        - Grammar and spelling
        - Completeness
        - Professional tone

        Provide a score (1-10) and list specific issues."""
    
    analysis = analyzer_llm.invoke(prompt)
    
    print(f"   Quality Score: {analysis.score}/10")
    print(f"   Issues Found: {len(analysis.issues)}")
    
    return {
        "processing_stage": "analysis_complete",
        "quality_score": analysis.score,
        "issues_found": analysis.issues,
        "approved": analysis.recommendation == "approve"
    }


# Node 3: Revision
def revise_document(state: DocumentState):
    """Revise document based on issues"""
    print(f"\n✏️  REVISION: Improving document...")
    
    issues_text = "\n".join([f"- {issue}" for issue in state['issues_found']])
    
    prompt = f"""Revise this document to address these issues:

        Original:
        {state['document_content']}

        Issues to fix:
        {issues_text}

        Provide an improved version (keep it concise, around same length)."""
    
    revised_content = llm.invoke(prompt).content
    
    print(f"Revisions applied: {len(state['issues_found'])} issues addressed")
    
    return {
        "processing_stage": "revision_complete",
        "document_content": revised_content,
        "revisions_made": state['issues_found']  # Track what was revised
    }


# Node 4: Final Approval
def finalize_document(state: DocumentState):
    """Mark document as complete"""
    print(f"\n✅ FINALIZED: Document approved and ready")
    
    return {
        "processing_stage": "finalized",
        "approved": True
    }


# Routing
def route_after_analysis(state: DocumentState) -> Literal["revise", "finalize"]:
    """Decide if revision is needed"""
    if state["quality_score"] >= 8:
        print("\n→ Routing to finalize (high quality)")
        return "finalize"
    else:
        print("\n→ Routing to revise (needs improvement)")
        return "revise"
    

# Build graph
builder = StateGraph(DocumentState)

builder.add_node("intake", intake_document)
builder.add_node("analyze", analyze_quality)
builder.add_node("revise", revise_document)
builder.add_node("finalize", finalize_document)

builder.add_edge(START, "intake")
builder.add_edge("intake", "analyze")
builder.add_conditional_edges(
    "analyze",
    route_after_analysis,
    {
        "revise": "revise",
        "finalize": "finalize"
    }
)
builder.add_edge("revise", "analyze")  # Re-analyze after revision
builder.add_edge("finalize", END)


# Compile with checkpointer
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)


# ==================================================================
# INITIAL EXECUTION
# ==================================================================

thread_id = "doc_review_001"

config = {"configurable": {"thread_id": thread_id}}

initial_input = {
    "document_title": "Is Messi the GOAT?",
    "document_content": "Yes, he won the 2022 World Cup with Argentina, cementing his legacy forever.",
    "processing_stage": "submitted",
    "quality_score": 0,
    "issues_found": [],
    "revisions_made": [],
    "approved": False
}

result = graph.invoke(initial_input, config=config)


""" Retrieving State """
def print_snapshot_data(snapshot_state):

    thread_id = snapshot_state.config["configurable"]["thread_id"]
    print(f"Thread ID: {thread_id}")

    checkpoint_id = snapshot_state.config["configurable"]["checkpoint_id"]
    print(f"Checkpoint ID: {checkpoint_id}")

    next_nodes = snapshot_state.next if snapshot_state.next else "None (workflow complete)"
    print(f"Next Nodes -> {next_nodes}")

    print(f"\nState Values:")
    print(f"Title: {snapshot_state.values.get('document_title', 'N/A')}")
    print(f"Stage: {snapshot_state.values.get('processing_stage', 'N/A')}")
    print(f"Quality Score: {snapshot_state.values.get('quality_score', 0)}")
    print(f"Approved: {snapshot_state.values.get('approved', False)}")
    print(f"Issues Found: {snapshot_state.values.get('issues_found', 'None')}")

print("-"* 50)
print("Current Graph State")
print("-"* 50)

# 1st Test
# current_state = graph.get_state(config)
# print_snapshot_data(current_state)

# 2nd Test
"""
print("-"* 50)
print("Full State History")
print("-"* 50)

history = list(graph.get_state_history(config))

total_checkpoints = len(history)
print(f"Total Checkpoints: {total_checkpoints}")

print("Checkpoint Timeline (newest to oldest)")
print("="*50)

for i, checkpoint in enumerate(history):
    print(f"\n\n{'*'*30}")
    print(f"Checkpoint Snapshot: {total_checkpoints - i}:")
    print(f"{'*'*30}")
    print_snapshot_data(checkpoint)
"""


# 3rd Test
""" Replaying State from analysis step"""
# input [0] -> start [1] -> intake [2] -> analyze [3]
"""
print('\n\n ----Replaying State from analysis step---')
history = list(graph.get_state_history(config))

analyze_checkpoint = history[3]

analyze_checkpoint_id = analyze_checkpoint.config["configurable"]["checkpoint_id"]

replay_config = {
    "configurable": {
        "thread_id": thread_id,
        "checkpoint_id": analyze_checkpoint_id
    }
}


print(f"\n Replaying from: {analyze_checkpoint_id}...")
print("This will re-evaluate: analyze -> revise -> analyze -> finalize")

replay = graph.invoke(None, replay_config)

print(f"✅ Replay Complete")
print(f"Final Stage: {replay['processing_stage']}")
print(f"Quality Score: {replay['quality_score']}/10")
"""

""" Updating State """

current_state = graph.get_state(config)

print("-"*50)
print("Current State (Before Manual Override)")
print("-"*50)
print_snapshot_data(current_state)

print("\n Manual Override: Document Approval")

graph.update_state(
    config,
    {
        "quality_score": 9,
        "approved": True,
        "processing_stage": "manually_approved",
        "issues_found": []
    }
)

updated_state = graph.get_state(config)

print("-"*50)
print("Updated State (After Manual Override)")
print("-"*50)
print_snapshot_data(updated_state)