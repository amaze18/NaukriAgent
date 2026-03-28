"""
LangGraph node functions for HuggingFace vLLM inference.
Parallel implementation to nodes.py using Qwen3.5-Claude-Opus model.

This uses the same 6-node workflow but with HuggingFace models
instead of local Ollama models.
"""

import re
from state import AgentState
from agents_hf import run_analysis_crew_hf
from config_hf import get_hf_slm_with_reasoning, DEFAULT_SCORE_THRESHOLD


# --- NODE 1: INPUT VALIDATION ---
def validate_inputs_hf(state: AgentState) -> AgentState:
    """
    Node 1: Validate input resume and job description (HF version).
    
    Args:
        state (AgentState): Current workflow state.
    
    Returns:
        AgentState: Updated state with validation result.
    
    Raises:
        ValueError: If resume or JD is missing.
    """
    print("=" * 60)
    print("NODE 1: VALIDATING INPUTS (HuggingFace vLLM)")
    print("=" * 60)
    
    if not state.get("resume") or not state["resume"].strip():
        raise ValueError("Resume is missing or empty")
    
    if not state.get("jd") or not state["jd"].strip():
        raise ValueError("Job description is missing or empty")
    
    print(f"✓ Resume received ({len(state['resume'])} characters)")
    print(f"✓ JD received ({len(state['jd'])} characters)")
    print(f"✓ Candidate: {state.get('candidate_name', 'Unknown')}")
    print(f"✓ Using: Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled")
    
    return state


# --- NODE 2 & 3: HUGGINGFACE CREWAI ANALYSIS ---
def run_crew_analysis_hf(state: AgentState) -> AgentState:
    """
    Nodes 2 & 3: Run CrewAI with HuggingFace inference.
    Uses Qwen3.5 reasoning model for deep analysis.
    
    Args:
        state (AgentState): Current workflow state.
    
    Returns:
        AgentState: Updated state with analysis and scores.
    """
    print("\n" + "=" * 60)
    print("NODES 2 & 3: HUGGINGFACE CREWAI ANALYSIS")
    print("=" * 60)
    
    try:
        slm = get_hf_slm_with_reasoning()
        print("CrewAI agents initialized with HuggingFace vLLM backend")
        print(f"Model: Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled")
        print("Reasoning mode: ENABLED")
        
        # Run the crew analysis with reasoning
        analysis_result = run_analysis_crew_hf(
            resume=state["resume"],
            jd=state["jd"],
            slm=slm,
            use_reasoning=True,
            include_skill_assessment=True
        )
        
        print("\n✓ HuggingFace CrewAI analysis completed")
        
        # Extract scores from analysis
        skill_score = extract_skill_score_hf(analysis_result)
        experience_score = extract_experience_score_hf(analysis_result)
        overall_score = int((skill_score + experience_score) / 2)
        
        print(f"  - Skill Match Score: {skill_score}%")
        print(f"  - Experience Match Score: {experience_score}%")
        print(f"  - Overall Score: {overall_score}%")
        
        state["analysis_results"] = analysis_result
        state["skill_match_score"] = skill_score
        state["experience_match_score"] = experience_score
        
        return state
        
    except Exception as e:
        print(f"✗ HuggingFace CrewAI analysis failed: {e}")
        raise


# --- NODE 4: SCORING & RANKING (HF VERSION) ---
def scoring_engine_hf(state: AgentState) -> AgentState:
    """
    Node 4: Advanced scoring using HuggingFace analysis.
    
    Args:
        state (AgentState): Current workflow state.
    
    Returns:
        AgentState: Updated state with final scores.
    """
    print("\n" + "=" * 60)
    print("NODE 4: SCORING & RANKING (HuggingFace Enhanced)")
    print("=" * 60)
    
    skill_score = state.get("skill_match_score", 0)
    experience_score = state.get("experience_match_score", 0)
    
    # Weighted scoring (from HF reasoning analysis)
    overall_score = int(
        (skill_score * 0.6) +  # Skills weighted more heavily
        (experience_score * 0.4)
    )
    
    # Apply reasoning-based adjustments (from analysis)
    reasoning_boost = extract_reasoning_confidence(state.get("analysis_results", ""))
    adjusted_score = int(overall_score * (1 + reasoning_boost / 100))
    adjusted_score = min(100, adjusted_score)
    
    state["overall_score"] = adjusted_score
    
    print(f"Base Score: {overall_score}%")
    print(f"Reasoning Confidence Boost: {reasoning_boost}%")
    print(f"Final Score: {adjusted_score}%")
    print(f"Threshold: {DEFAULT_SCORE_THRESHOLD}%")
    
    if adjusted_score >= DEFAULT_SCORE_THRESHOLD:
        print(f"✓ Candidate meets threshold - PROCEED to approval")
    else:
        print(f"✗ Candidate below threshold - Flag for manual review")
    
    return state


# --- NODE 5: HUMAN APPROVAL (HF VERSION) ---
def human_approval_hf(state: AgentState) -> AgentState:
    """
    Node 5: Human-in-the-loop approval with HF analysis.
    
    Args:
        state (AgentState): Current workflow state.
    
    Returns:
        AgentState: Updated with recruiter decision.
    """
    print("\n" + "=" * 60)
    print("NODE 5: HUMAN APPROVAL (With HuggingFace Analysis)")
    print("=" * 60)
    
    candidate = state.get("candidate_name", "Unknown")
    score = state.get("overall_score", 0)
    
    print(f"\nCandidate: {candidate}")
    print(f"Email: {state.get('candidate_email', 'N/A')}")
    print(f"Final Score (HF Analysis): {score}%")
    print(f"\nAnalysis Summary (from Qwen3.5-Opus reasoning):")
    print("-" * 40)
    
    analysis = state.get("analysis_results", "No analysis available")
    display_analysis = analysis[:800] + "..." if len(analysis) > 800 else analysis
    print(display_analysis)
    print("-" * 40)
    
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
        state["recruiter_notes"] = "Additional information requested - Use HF model for deeper analysis"
        print("⊘ Marked for additional review")
    
    return state


# --- NODE 6: FINALIZATION (HF VERSION) ---
def generate_shortlist_hf(state: AgentState) -> AgentState:
    """
    Node 6: Finalize candidate decision (HF version).
    
    Args:
        state (AgentState): Current workflow state.
    
    Returns:
        AgentState: Final state with all details.
    """
    print("\n" + "=" * 60)
    print("NODE 6: GENERATING SHORTLIST & NOTIFICATIONS (HF Analysis)")
    print("=" * 60)
    
    candidate = state.get("candidate_name", "Unknown")
    status = state.get("status", "unknown")
    score = state.get("overall_score", 0)
    
    print(f"\nFinalizing: {candidate}")
    print(f"Status: {status.upper()}")
    print(f"Final Score: {score}% (from Qwen3.5-Claude-Opus reasoning)")
    
    if status == "approved":
        print(f"✓ Candidate shortlisted!")
        print(f"Email notification would be sent to: {state.get('candidate_email', 'N/A')}")
        print("Analysis Method: HuggingFace vLLM with Qwen3.5-Claude-Opus reasoning")
    elif status == "rejected":
        reason = state.get("rejection_reason", "Did not meet requirements")
        print(f"✗ Candidate rejection notice prepared")
        print(f"Reason: {reason}")
    
    print(f"\nRecruiter Notes: {state.get('recruiter_notes', 'None')}")
    print(f"Analysis Confidence: High (from Qwen3.5 reasoning chain)")
    
    return state


# --- HELPER FUNCTIONS FOR HF ANALYSIS ---
def extract_skill_score_hf(analysis: str) -> float:
    """
    Extract skill match score from HuggingFace analysis output.
    
    Args:
        analysis (str): The analysis text from Qwen3.5 model.
    
    Returns:
        float: Skill match score (0-100).
    """
    patterns = [
        r'skill.*?match.*?(\d+)\s*%',
        r'(\d+)\s*%.*?skill.*?match',
        r'skill.*?alignment.*?(\d+)',
        r'technical.*?match.*?(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, analysis, re.IGNORECASE)
        if match:
            score = int(match.group(1))
            return min(100, max(0, score))
    
    # If no explicit score found, estimate from language
    if "strong match" in analysis.lower() or "excellent skills" in analysis.lower():
        return 85.0
    elif "moderate match" in analysis.lower() or "good match" in analysis.lower():
        return 75.0
    elif "weak match" in analysis.lower() or "missing" in analysis.lower():
        return 50.0
    
    return 75.0


def extract_experience_score_hf(analysis: str) -> float:
    """
    Extract experience match score from HuggingFace analysis.
    
    Args:
        analysis (str): The analysis text from Qwen3.5 model.
    
    Returns:
        float: Experience match score (0-100).
    """
    patterns = [
        r'experience.*?match.*?(\d+)\s*%',
        r'(\d+)\s*%.*?experience.*?match',
        r'experience.*?alignment.*?(\d+)',
        r'years.*?match.*?(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, analysis, re.IGNORECASE)
        if match:
            score = int(match.group(1))
            return min(100, max(0, score))
    
    # Estimate from language
    if "years of experience align" in analysis.lower():
        return 80.0
    elif "sufficient experience" in analysis.lower():
        return 70.0
    elif "less experience" in analysis.lower():
        return 55.0
    
    return 70.0


def extract_reasoning_confidence(analysis: str) -> float:
    """
    Extract reasoning confidence/quality score from analysis.
    Used for score adjustment based on reasoning chain depth.
    
    Args:
        analysis (str): The analysis text.
    
    Returns:
        float: Confidence boost percentage (-20 to +20).
    """
    # Look for reasoning quality indicators
    reasoning_indicators = {
        "thorough analysis": 10,
        "strong recommendation": 8,
        "clear reasoning": 7,
        "well-structured": 6,
        "structured thinking": 8,
        "deep analysis": 10,
        "comprehensive": 8,
        "minimal concerns": 5,
    }
    
    negative_indicators = {
        "significant gaps": -15,
        "poor fit": -20,
        "major concerns": -15,
        "weak": -10,
        "insufficient": -12,
    }
    
    boost = 0.0
    
    # Check positive indicators
    for indicator, score in reasoning_indicators.items():
        if indicator in analysis.lower():
            boost += score
    
    # Check negative indicators
    for indicator, score in negative_indicators.items():
        if indicator in analysis.lower():
            boost += score
    
    # Cap between -20 and +20
    return max(-20, min(20, boost))


# --- DIAGNOSTIC FUNCTION ---
def analyze_reasoning_chain(state: AgentState) -> dict:
    """
    Extract and analyze the reasoning chain from HF model output.
    Useful for debugging and understanding model reasoning.
    
    Args:
        state (AgentState): Workflow state with analysis results.
    
    Returns:
        dict: Extracted reasoning components.
    """
    analysis = state.get("analysis_results", "")
    
    # Extract thinking blocks if present
    thinking_blocks = re.findall(r'<think>(.*?)</think>', analysis, re.DOTALL)
    
    return {
        "has_thinking_blocks": len(thinking_blocks) > 0,
        "thinking_blocks": thinking_blocks,
        "analysis_length": len(analysis),
        "reasoning_present": "Let me analyze" in analysis or "<think>" in analysis,
        "skill_score": state.get("skill_match_score", 0),
        "experience_score": state.get("experience_match_score", 0),
        "overall_score": state.get("overall_score", 0),
    }
