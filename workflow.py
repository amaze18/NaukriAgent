"""
LangGraph workflow builder for NaukriAgent.
Constructs the state graph and defines the workflow logic.
"""

from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes import (
    validate_inputs,
    run_crew_analysis,
    scoring_engine,
    human_approval,
    generate_shortlist
)


def build_workflow():
    """
    Build the LangGraph workflow state machine.
    
    Workflow Nodes:
        1. validate_inputs: Validate resume and JD
        2. run_crew_analysis: Run CrewAI agents (Nodes 2 & 3)
        3. scoring_engine: Calculate scores (Node 4)
        4. human_approval: Get recruiter approval (Node 5)
        5. generate_shortlist: Finalize decision (Node 6)
    
    Edges:
        START -> validate -> crew_analysis -> scoring -> approval
        approval -> [finalize (if approved) | END (if rejected)]
        finalize -> END
    
    Returns:
        Compiled LangGraph workflow application.
    """
    
    workflow = StateGraph(AgentState)
    
    # Add all nodes to the graph
    workflow.add_node("validate", validate_inputs)
    workflow.add_node("crew_analysis", run_crew_analysis)
    workflow.add_node("scoring", scoring_engine)
    workflow.add_node("approval", human_approval)
    workflow.add_node("finalize", generate_shortlist)
    
    # Define edges (connections between nodes)
    workflow.add_edge(START, "validate")
    workflow.add_edge("validate", "crew_analysis")
    workflow.add_edge("crew_analysis", "scoring")
    workflow.add_edge("scoring", "approval")
    
    # Conditional edge: Approval decision
    # If approved -> finalize, otherwise -> END (rejection)
    def route_decision(state: AgentState):
        """
        Route workflow based on recruiter approval decision.
        
        Args:
            state (AgentState): Current workflow state.
        
        Returns:
            str: Next node ("finalize" for approved, END for rejected/pending).
        """
        if state.get("status") == "approved":
            return "finalize"
        else:
            return "end"
    
    workflow.add_conditional_edges(
        "approval",
        route_decision,
        {
            "finalize": "finalize",
            "end": END
        }
    )
    
    workflow.add_edge("finalize", END)
    
    # Compile the workflow into an executable application
    app = workflow.compile()
    
    return app


def get_compiled_app():
    """
    Get the compiled LangGraph application.
    
    Returns:
        Compiled LangGraph workflow app ready for execution.
    """
    return build_workflow()
