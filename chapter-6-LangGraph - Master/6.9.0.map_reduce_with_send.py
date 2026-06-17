from typing import TypedDict, Annotated, List
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

class OverallState(TypedDict):
    topic: str
    subtopics: List[str]
    research_results: Annotated[List[str], add]
    final_report: str

class ResearchState(TypedDict):
    subtopic: str
    research_results: List[str]

def generate_subtopics(state: OverallState):
    topic = state['topic']

    subtopics = [
        f"{topic} - History",
        f"{topic} - Current Trends",
        f"{topic} - Future Outlook"
    ]

    return {
        "subtopics": subtopics
    }

def research_subtopic(state: ResearchState):
    subtopic = state['subtopic']
    result = f"Research finding on '{subtopic}': [detailed analysis, data, insights,...]"

    return {
        "research_results": [result]
    }

def compile_report(state: OverallState):
    results = state['research_results']
    report = "=" * 50 + "\n"
    report += "COMPREHENSIVE RESEARCH REPORT"
    report = "=" * 50 + "\n"

    for i, result in enumerate(results, 1):
        report += f"{i}. {result}\n"

    return {
        "final_report": report
    }

def continue_to_research(state: OverallState):
    return [
        Send("research_subtopic", {"subtopic": s}) for s in state["subtopics"]
    ]

builder = StateGraph(OverallState)

builder.add_node(generate_subtopics)
builder.add_node(research_subtopic)
builder.add_node(compile_report)

builder.add_edge(START, "generate_subtopics")
builder.add_conditional_edges("generate_subtopics", continue_to_research)
builder.add_edge("research_subtopic", "compile_report")
builder.add_edge("compile_report", END)

graph = builder.compile()

"""Test the Graph"""

initial_state = {
    "topic": "Artificial Intelligence",
    "subtopics": [],
    "research_results": [],
    "final_report": ""
}

final_state = graph.invoke(initial_state)

print("Final State: ")
print(final_state)
