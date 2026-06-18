from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

class ComplaintState(TypedDict):
    complaint: str
    category: Optional[str]
    validation_result: Optional[str]
    investigation_result: Optional[str]
    resolution: Optional[str]
    effectiveness: Optional[str]
    outcome: Optional[str]
    workflow_path: List[str]
    status: str

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

workflow = StateGraph(ComplaintState)

def intake_node(state: ComplaintState) -> ComplaintState:
    """Step 1: Intake - Parse and categorize the complaint"""
    print("\n[INTAKE] Processing complaint...")
    
    complaint = state["complaint"]
    
    # Categorize complaint using LLM
    categorization_prompt = f"""Categorize this Downside Up complaint into one of these categories:
- portal: Issues with portal timing, location, or behavior
- monster: Issues with creature behavior (demogorgons, etc.)
- psychic: Issues with psychic abilities or limitations
- environmental: Issues with electricity, weather, or physical environment
- other: Anything else
 
Complaint: {complaint}
 
Respond with ONLY the category name (portal, monster, psychic, environmental, or other)."""
 
    response = llm.invoke([HumanMessage(content=categorization_prompt)])
    category = response.content.strip().lower()
    
    # Update state
    new_state = {
        **state,
        "category": category,
        "workflow_path": state.get("workflow_path", []) + ["intake"],
        "status": "intake"
    }
    
    print(f"[INTAKE] Categorized as: {category}")
    return new_state

def validate_node(state: ComplaintState) -> ComplaintState:
    """Step 2: Validate complaint against protocol rules"""
    print("\n[VALIDATE] Validating complaint...")

    category = state["category"]
    complaint = state["complaint"]

    validation_result = "valid"

    if category == "other":
        validation_result = "invalid"

    if len(complaint) < 20:
        validation_result = "invalid"

    new_state = {
        **state,
        "validation_result": validation_result,
        "workflow_path": state["workflow_path"] + ["validate"],
        "status": "validate"
    }

    print(f"[VALIDATE] Result: {validation_result}")
    return new_state

def investigate_node(state: ComplaintState) -> ComplaintState:
    """Step 3: Investigate complaint"""
    print("\n[INVESTIGATE] Investigating complaint...")

    category = state["category"]

    investigation_result = (
        f"Investigation completed for {category} complaint. "
        f"Evidence documented according to Downside Up protocol."
    )

    new_state = {
        **state,
        "investigation_result": investigation_result,
        "workflow_path": state["workflow_path"] + ["investigate"],
        "status": "investigate"
    }

    print("[INVESTIGATE] Investigation complete")
    return new_state

def resolve_node(state: ComplaintState) -> ComplaintState:
    """Step 4: Resolve complaint"""
    print("\n[RESOLVE] Creating resolution...")

    category = state["category"]

    resolution = f"Applied standard Downside Up protocol for {category} issues."
    effectiveness = "medium"

    new_state = {
        **state,
        "resolution": resolution,
        "effectiveness": effectiveness,
        "workflow_path": state["workflow_path"] + ["resolve"],
        "status": "resolve"
    }

    print(f"[RESOLVE] Effectiveness: {effectiveness}")
    return new_state

def close_node(state: ComplaintState) -> ComplaintState:
    """Step 5: Close complaint"""
    print("\n[CLOSE] Closing complaint...")

    outcome = "Resolution applied and logged"

    new_state = {
        **state,
        "outcome": outcome,
        "workflow_path": state["workflow_path"] + ["close"],
        "status": "closed"
    }

    print("[CLOSE] Complaint closed")
    return new_state

# Build the LangGraph complaint workflow
# Complaints must follow Bloyce's Protocol:
# intake -> validate -> investigate -> resolve -> close

def validation_router(state: ComplaintState):
    """Route complaints based on validation result"""

    if state["validation_result"] == "invalid":
        return "close"

    return "investigate"

workflow.add_node("intake", intake_node)
workflow.add_node("validate", validate_node)
workflow.add_node("investigate", investigate_node)
workflow.add_node("resolve", resolve_node)
workflow.add_node("close", close_node)

workflow.set_entry_point("intake")

workflow.add_edge("intake", "validate")
workflow.add_conditional_edges(
    "validate",
    validation_router,
    {
        "investigate": "investigate",
        "close": "close"
    }
)
workflow.add_edge("investigate", "resolve")
workflow.add_edge("resolve", "close")
workflow.add_edge("close", END)

app = workflow.compile()

test_complaints = [
    "The Downside Up portal opens at different times each day. How do I predict when?",
    "Why do creatures and power lines react strangely together?",
    "Random thing"
]

print("\nTesting workflow with sample complaints...\n")

for complaint in test_complaints:

    test_state = {
        "complaint": complaint,
        "category": None,
        "validation_result": None,
        "investigation_result": None,
        "resolution": None,
        "effectiveness": None,
        "outcome": None,
        "workflow_path": [],
        "status": "new"
    }

    result = app.invoke(test_state)

    print("\nWorkflow Path:")
    print(result["workflow_path"])