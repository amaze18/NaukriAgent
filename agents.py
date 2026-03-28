"""
CrewAI agents and crew setup for NaukriAgent.
Defines the specialized agents for resume analysis and JD matching.
"""

from crewai import Agent, Task, Crew
from config import get_slm


def get_resume_analyzer(slm):
    """
    Create the Resume Analyzer agent.
    
    Args:
        slm: The language model instance to use.
    
    Returns:
        Agent: Configured Resume Analyzer agent.
    """
    return Agent(
        role="Resume Analyzer",
        goal="Extract and identify key technical skills, experience, "
             "certifications, and qualifications from the resume",
        backstory="You are an expert HR specialist with deep knowledge of "
                  "technical talent assessment. You excel at parsing resumes "
                  "and identifying relevant experience.",
        llm=slm,
        verbose=True
    )


def get_jd_matcher(slm):
    """
    Create the JD Requirement Matcher agent.
    
    Args:
        slm: The language model instance to use.
    
    Returns:
        Agent: Configured JD Matcher agent.
    """
    return Agent(
        role="JD Requirement Matcher",
        goal="Compare candidate skills and experience against job description "
             "requirements and identify gaps or strengths",
        backstory="You are a specialist in candidate-job alignment with years "
                  "of experience in technical recruitment. You provide detailed "
                  "analysis on how well a candidate fits a position.",
        llm=slm,
        verbose=True
    )


def create_analysis_crew(slm, resume: str, jd: str):
    """
    Create and configure the CrewAI crew for candidate analysis.
    
    Args:
        slm: The language model instance to use.
        resume (str): The candidate's resume content.
        jd (str): The job description.
    
    Returns:
        Crew: Configured crew with tasks for analysis.
    """
    analyzer = get_resume_analyzer(slm)
    matcher = get_jd_matcher(slm)
    
    # Task 1: Resume Analysis
    analyze_task = Task(
        description=f"""Analyze the following resume and extract all relevant information:
        
        RESUME:
        {resume}
        
        Provide a comprehensive breakdown including:
        - Technical skills and proficiency levels
        - Years of relevant experience
        - Key achievements and accomplishments
        - Certifications and qualifications
        - Technologies and tools expertise""",
        expected_output="Detailed resume analysis with categorized skills and experience",
        agent=analyzer
    )
    
    # Task 2: JD Matching
    match_task = Task(
        description=f"""Compare the candidate's profile from the resume analysis against the job description.
        
        JOB DESCRIPTION:
        {jd}
        
        Provide a detailed assessment including:
        - Skills alignment (what matches, what's missing)
        - Experience level alignment
        - Certification requirements met
        - Overall fit assessment (percentage match)
        - Top 3 strengths for this role
        - Top 3 concerns or gaps""",
        expected_output="Detailed JD matching analysis with alignment scores",
        agent=matcher
    )
    
    crew = Crew(
        agents=[analyzer, matcher],
        tasks=[analyze_task, match_task],
        verbose=True
    )
    
    return crew


def run_analysis_crew(resume: str, jd: str, slm):
    """
    Execute the CrewAI crew to analyze a candidate.
    
    Args:
        resume (str): The candidate's resume content.
        jd (str): The job description.
        slm: The language model instance to use.
    
    Returns:
        str: Complete analysis results from the crew.
    
    Raises:
        Exception: If crew execution fails.
    """
    try:
        crew = create_analysis_crew(slm, resume, jd)
        result = crew.kickoff()
        return str(result)
    except Exception as e:
        raise Exception(f"CrewAI analysis failed: {e}")
