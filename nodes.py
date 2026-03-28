"""
LangGraph node functions for the NaukriAgent workflow.
Defines the processing logic for each node in the workflow.
"""

import re
from state import AgentState
from agents import run_analysis_crew
from config import get_slm, DEFAULT_SCORE_THRESHOLD


# --- NODE 1: INPUT VALIDATION ---
def validate_inputs(state: AgentState) -> AgentState:
    """
    Node 1: Validate input resume and job description.
    Ensures both required inputs are provided and non-empty.
    
    Args:
        state (AgentState): Current workflow state.
    
    Returns:
        AgentState: Updated state with validation result.
    
    Raises:
        ValueError: If resume or JD is missing.
    """
    print("=" * 60)
    print("NODE 1: VALIDATING INPUTS")
    print("=" * 60)
    
    if not state.get("resume") or not state["resume"].strip():
        raise ValueError("Resume is missing or empty")
    
    if not state.get("jd") or not state["jd"].strip():
        raise ValueError("Job description is missing or empty")
    
    print(f"✓ Resume received ({len(state['resume'])} characters)")
    print(f"✓ JD received ({len(state['jd'])} characters)")
    print(f"✓ Candidate: {state.get('candidate_name', 'Unknown')}")
    
    return state


# --- NODE 2 & 3: CREWAI ANALYSIS ---
def run_crew_analysis(state: AgentState) -> AgentState:
    """
    Nodes 2 & 3: Run CrewAI agents for resume analysis and JD matching.
    Uses two specialized agents to analyze the candidate profile.
    
    Args:
        state (AgentState): Current workflow state.
    
    Returns:
        AgentState: Updated state with analysis results and scores.
    """
    print("\n" + "=" * 60)
    print("NODES 2 & 3: CREWAI ANALYSIS")
    print("=" * 60)
    
    try:
        slm = get_slm()
        print("Initializing CrewAI agents...")
        
        # Run the crew analysis
        analysis_result = run_analysis_crew(
            resume=state["resume"],
            jd=state["jd"],
            slm=slm
        )
        
        print("\n✓ CrewAI analysis completed")
        
        # Extract scores from analysis (mock scoring for now)
        # In production, parse the actual analysis to extract scores
        skill_score = extract_skill_score(analysis_result)
        experience_score = extract_experience_score(analysis_result)
        overall_score = int((skill_score + experience_score) / 2)
        
        print(f"  - Skill Match Score: {skill_score}%")
        print(f"  - Experience Match Score: {experience_score}%")
        print(f"  - Overall Score: {overall_score}%")
        
        state["analysis_results"] = analysis_result
        state["skill_match_score"] = skill_score
        state["experience_match_score"] = experience_score
        
        return state
        
    except Exception as e:
        print(f"✗ CrewAI analysis failed: {e}")
        raise


# --- NODE 4: SCORING & RANKING ---
def scoring_engine(state: AgentState) -> AgentState:
    """
    Node 4: Advanced scoring and ranking logic.
    Processes the CrewAI analysis to generate a final score.
    
    Args:
        state (AgentState): Current workflow state.
    
    Returns:
        AgentState: Updated state with final overall score.
    """
    print("\n" + "=" * 60)
    print("NODE 4: SCORING & RANKING")
    print("=" * 60)
    
    # Extract scores already set by CrewAI analysis
    skill_score = state.get("skill_match_score", 0)
    experience_score = state.get("experience_match_score", 0)
    
    # Weighted scoring (adjust weights as needed)
    overall_score = int(
        (skill_score * 0.6) +  # Skills weighted more heavily
        (experience_score * 0.4)
    )
    
    state["overall_score"] = overall_score
    
    print(f"Calculated Score: {overall_score}%")
    print(f"Threshold: {DEFAULT_SCORE_THRESHOLD}%")
    
    if overall_score >= DEFAULT_SCORE_THRESHOLD:
        print(f"✓ Candidate meets threshold - PROCEED to approval")
    else:
        print(f"✗ Candidate below threshold - Flag for manual review")
    
    return state


# --- NODE 5: HUMAN-IN-THE-LOOP APPROVAL ---
def human_approval(state: AgentState) -> AgentState:
    """
    Node 5: Human-in-the-loop approval gate.
    Pauses workflow for recruiter review and decision.
    
    In production, this would integrate with a UI that allows
    recruiters to review the analysis and make decisions.
    
    Args:
        state (AgentState): Current workflow state.
    
    Returns:
        AgentState: Updated state with recruiter decision.
    """
    print("\n" + "=" * 60)
    print("NODE 5: HUMAN APPROVAL")
    print("=" * 60)
    
    candidate = state.get("candidate_name", "Unknown")
    score = state.get("overall_score", 0)
    
    print(f"\nCandidate: {candidate}")
    print(f"Overall Score: {score}%")
    print(f"\nAnalysis Summary:")
    print("-" * 40)
    # Print first 500 chars of analysis
    analysis = state.get("analysis_results", "No analysis available")
    print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
    print("-" * 40)
    
    # In a real app, this would wait for UI input
    # For now, we simulate with interactive input
    print("\nOptions:")
    print("  1. Approve")
    print("  2. Reject")
    print("  3. Request More Info")
    
    user_input = input("\nEnter your decision (approve/reject/info): ").lower().strip()
    
    if user_input == "approve":
        state["status"] = "approved"
        state["recruiter_notes"] = input("Add any notes (optional): ").strip()
        print("✓ Candidate APPROVED")
    elif user_input == "reject":
        state["status"] = "rejected"
        state["rejection_reason"] = input("Reason for rejection: ").strip()
        print("✗ Candidate REJECTED")
    else:
        state["status"] = "pending"
        state["recruiter_notes"] = "Additional information requested"
        print("⊘ Marked for additional review")
    
    return state


# --- NODE 6: FINALIZATION ---
def generate_shortlist(state: AgentState) -> AgentState:
    """
    Node 6: Finalize candidate decision and prepare shortlist.
    Generates notifications and updates final candidate status.
    
    Args:
        state (AgentState): Current workflow state.
    
    Returns:
        AgentState: Final state with all details.
    """
    print("\n" + "=" * 60)
    print("NODE 6: GENERATING SHORTLIST & NOTIFICATIONS")
    print("=" * 60)
    
    candidate = state.get("candidate_name", "Unknown")
    status = state.get("status", "unknown")
    score = state.get("overall_score", 0)
    
    print(f"\nFinalizing: {candidate}")
    print(f"Status: {status.upper()}")
    print(f"Final Score: {score}%")
    
    if status == "approved":
        print(f"✓ Candidate shortlisted!")
        print(f"Email notification would be sent to: {state.get('candidate_email', 'N/A')}")
    elif status == "rejected":
        reason = state.get("rejection_reason", "Did not meet requirements")
        print(f"✗ Candidate rejection notice prepared")
        print(f"Reason: {reason}")
    
    print(f"\nNotes from recruiter: {state.get('recruiter_notes', 'None')}")
    
    return state


# --- HELPER FUNCTIONS ---
def extract_skill_score(analysis: str) -> float:
    """
    Extract skill match score from CrewAI analysis.
    Uses regex to find score patterns in the text.
    
    Args:
        analysis (str): The analysis text from CrewAI.
    
    Returns:
        float: Extracted skill score (0-100).
    """
    # Look for patterns like "85% skill match" or "Skill Match: 85"
    patterns = [
        r'skill.*?(\d+)\s*%',
        r'(\d+)\s*%.*?skill',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, analysis, re.IGNORECASE)
        if match:
            score = int(match.group(1))
            return min(100, max(0, score))
    
    # Default to 75 if no score found
    return 75.0


def extract_experience_score(analysis: str) -> float:
    """
    Extract experience match score from CrewAI analysis.
    Uses regex to find score patterns in the text.
    
    Args:
        analysis (str): The analysis text from CrewAI.
    
    Returns:
        float: Extracted experience score (0-100).
    """
    # Look for patterns like "80% experience match" or "Experience Match: 80"
    patterns = [
        r'experience.*?(\d+)\s*%',
        r'(\d+)\s*%.*?experience',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, analysis, re.IGNORECASE)
        if match:
            score = int(match.group(1))
            return min(100, max(0, score))
    
    # Default to 70 if no score found
    return 70.0
