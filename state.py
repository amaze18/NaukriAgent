"""
State definition for the NaukriAgent workflow.
Defines the AgentState TypedDict that flows through the LangGraph.
"""

from typing import TypedDict, Literal


class AgentState(TypedDict):
    """
    Represents the state of a candidate evaluation workflow.
    
    Attributes:
        resume (str): The candidate's resume content.
        jd (str): The job description.
        analysis_results (str): Detailed analysis from CrewAI agents.
        skill_match_score (float): Matching score for skills (0-100).
        experience_match_score (float): Matching score for experience (0-100).
        overall_score (int): Overall ranking score (0-100).
        status (Literal): Current status of the evaluation.
        rejection_reason (str): Reason if candidate was rejected.
        recruiter_notes (str): Notes from the human recruiter.
        candidate_name (str): Name of the candidate (optional).
        candidate_email (str): Email of the candidate (optional).
    """
    resume: str
    jd: str
    analysis_results: str
    skill_match_score: float
    experience_match_score: float
    overall_score: int
    status: Literal["pending", "approved", "rejected"]
    rejection_reason: str
    recruiter_notes: str
    candidate_name: str
    candidate_email: str
