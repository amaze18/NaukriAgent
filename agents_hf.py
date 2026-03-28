"""
CrewAI agents for HuggingFace vLLM inference.
Uses Qwen3.5-Claude-Opus-Reasoning-Distilled model via vLLM.

This is an alternative to agents.py that uses HuggingFace models
instead of local Ollama-based models.
"""

from crewai import Agent, Task, Crew
from config_hf import get_hf_slm, get_hf_slm_with_reasoning


def get_resume_analyzer_hf(slm):
    """
    Create the Resume Analyzer agent (HF/vLLM version).
    Uses Qwen3.5 reasoning for detailed analysis.
    
    Args:
        slm: The HuggingFace language model instance.
    
    Returns:
        Agent: Configured Resume Analyzer agent with reasoning.
    """
    return Agent(
        role="Resume Analyzer",
        goal="Extract and identify key technical skills, experience, "
             "certifications, and qualifications from the resume. "
             "Use structured thinking to break down the candidate's background.",
        backstory="You are an expert HR specialist with deep knowledge of "
                  "technical talent assessment. You excel at parsing resumes, "
                  "identifying relevant experience, and ranking candidate strengths. "
                  "Your reasoning is structured and methodical, following "
                  "Claude-4.6-Opus's analytical approach.",
        llm=slm,
        verbose=True,
        allow_delegation=False
    )


def get_jd_matcher_hf(slm):
    """
    Create the JD Requirement Matcher agent (HF/vLLM version).
    Uses Qwen3.5 reasoning for detailed comparison.
    
    Args:
        slm: The HuggingFace language model instance.
    
    Returns:
        Agent: Configured JD Matcher agent with reasoning.
    """
    return Agent(
        role="JD Requirement Matcher",
        goal="Compare candidate skills and experience against job description "
             "requirements. Identify gaps, strengths, and provide an alignment score. "
             "Use structured reasoning to evaluate fit holistically.",
        backstory="You are a specialist in candidate-job alignment with years "
                  "of experience in technical recruitment. Your strength lies in "
                  "providing detailed, transparent analysis of how well a candidate "
                  "fits a position. You follow Claude-Opus's methodical thinking "
                  "patterns, breaking complex evaluations into clear components.",
        llm=slm,
        verbose=True,
        allow_delegation=False
    )


def get_skill_assessor_hf(slm):
    """
    Create an additional Skill Assessor agent for deeper analysis.
    
    Args:
        slm: The HuggingFace language model instance.
    
    Returns:
        Agent: Configured Skill Assessor agent.
    """
    return Agent(
        role="Technical Skill Assessor",
        goal="Deeply assess the technical proficiency and depth of candidate skills. "
             "Evaluate code quality, experience maturity, and framework expertise.",
        backstory="You are a technical engineer with expertise in various tech stacks. "
                  "You can evaluate code quality, understand technology depth, "
                  "and assess whether claimed skills match job requirements. "
                  "You provide transparent, reasoning-based technical assessments.",
        llm=slm,
        verbose=True,
        allow_delegation=False
    )


def create_analysis_crew_hf(slm, resume: str, jd: str, include_skill_assessment: bool = False):
    """
    Create and configure the CrewAI crew for HuggingFace model inference.
    
    Args:
        slm: The HuggingFace language model instance.
        resume (str): The candidate's resume content.
        jd (str): The job description.
        include_skill_assessment (bool): Include technical skill assessor.
    
    Returns:
        Crew: Configured crew with tasks for analysis.
    """
    analyzer = get_resume_analyzer_hf(slm)
    matcher = get_jd_matcher_hf(slm)
    
    # Task 1: Resume Analysis
    analyze_task = Task(
        description=f"""Analyze the following resume and extract all relevant information.
        Use your structured thinking to methodically break down the candidate's background.
        
        RESUME:
        {resume}
        
        Provide a comprehensive breakdown including:
        - Technical skills and proficiency levels
        - Years of relevant experience
        - Key achievements and accomplishments
        - Certifications and qualifications
        - Technologies and tools expertise
        - Employment history and progression
        - Notable projects or contributions""",
        expected_output="Detailed structured resume analysis with categorized skills, "
                       "experience timeline, and key competencies",
        agent=analyzer
    )
    
    # Task 2: JD Matching
    match_task = Task(
        description=f"""Compare the candidate's profile from the resume analysis against the job description.
        Use methodical reasoning to evaluate each requirement and provide transparent scores.
        
        JOB DESCRIPTION:
        {jd}
        
        Provide a detailed assessment including:
        - Skills alignment (what matches, what's missing, percentage match)
        - Experience level alignment (requirement vs candidate)
        - Certification requirements met/unmet
        - Overall fit assessment (provide a 0-100 percentage)
        - Top 3 strengths for this specific role
        - Top 3 concerns or gaps
        - Nice-to-have skills match
        - Final recommendation (Strong/Moderate/Weak fit)""",
        expected_output="Detailed JD matching analysis with explicit alignment scores, "
                       "fit assessment, and clear recommendations",
        agent=matcher
    )
    
    agents = [analyzer, matcher]
    tasks = [analyze_task, match_task]
    
    # Optional: Add technical skill assessor for deeper analysis
    if include_skill_assessment:
        skill_assessor = get_skill_assessor_hf(slm)
        
        skill_task = Task(
            description=f"""Perform a deep technical assessment of the candidate's skills.
            Focus on code quality indicators, framework expertise, and technology depth.
            
            Based on the resume: {resume}
            
            And requirements: {jd}
            
            Evaluate:
            - Coding proficiency indicators
            - Framework and library expertise
            - Problem-solving approach shown in projects
            - Technical debt awareness
            - Best practices adherence
            - Learning ability based on skill evolution""",
            expected_output="Technical depth assessment with proficiency scores "
                           "and capability evaluation",
            agent=skill_assessor
        )
        
        agents.append(skill_assessor)
        tasks.append(skill_task)
    
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True,
        memory=True  # Enable memory for context retention
    )
    
    return crew


def run_analysis_crew_hf(resume: str, jd: str, slm=None, use_reasoning: bool = True,
                        include_skill_assessment: bool = False):
    """
    Execute the CrewAI crew with HuggingFace inference.
    
    Args:
        resume (str): The candidate's resume content.
        jd (str): The job description.
        slm: The language model instance. If None, creates one.
        use_reasoning (bool): Use reasoning-optimized model.
        include_skill_assessment (bool): Include technical skill assessor.
    
    Returns:
        str: Complete analysis results from the crew.
    
    Raises:
        Exception: If crew execution fails.
    """
    try:
        # Initialize SLM if not provided
        if slm is None:
            if use_reasoning:
                slm = get_hf_slm_with_reasoning()
            else:
                slm = get_hf_slm()
        
        print("\n" + "=" * 70)
        print("INITIALIZING HUGGINGFACE CREWAI ANALYSIS")
        print("=" * 70)
        print("Initializing CrewAI agents with HuggingFace vLLM backend...")
        
        # Create and execute crew
        crew = create_analysis_crew_hf(
            slm=slm,
            resume=resume,
            jd=jd,
            include_skill_assessment=include_skill_assessment
        )
        
        print("Executing crew analysis...")
        result = crew.kickoff()
        
        print("\n✓ CrewAI analysis completed successfully")
        
        return str(result)
        
    except ConnectionError as e:
        print(f"\n✗ Connection error: {e}")
        raise
    except Exception as e:
        print(f"\n✗ CrewAI analysis failed: {e}")
        raise Exception(f"HuggingFace CrewAI analysis failed: {e}")


# --- UTILITY FUNCTIONS ---

def compare_analysis_approaches(resume: str, jd: str):
    """
    Compare analysis using standard and reasoning-enhanced approaches.
    Useful for benchmarking and quality evaluation.
    
    Args:
        resume (str): Candidate resume.
        jd (str): Job description.
    
    Returns:
        tuple: (standard_result, reasoning_result)
    """
    print("\nComparing analysis approaches...")
    
    # Standard analysis
    print("\n1. Standard Analysis (without reasoning optimization)...")
    slm_standard = get_hf_slm()
    result_standard = run_analysis_crew_hf(
        resume=resume,
        jd=jd,
        slm=slm_standard,
        use_reasoning=False
    )
    
    # Reasoning analysis
    print("\n2. Reasoning-Enhanced Analysis...")
    slm_reasoning = get_hf_slm_with_reasoning()
    result_reasoning = run_analysis_crew_hf(
        resume=resume,
        jd=jd,
        slm=slm_reasoning,
        use_reasoning=True,
        include_skill_assessment=True
    )
    
    return result_standard, result_reasoning


if __name__ == "__main__":
    # Example usage
    from config_hf import print_model_info
    
    print_model_info()
    
    sample_resume = """
    Alice Johnson
    Senior Backend Engineer with 8 years experience
    
    Skills: Python, Go, Kubernetes, AWS, PostgreSQL, Redis, Docker
    Experience: Built scalable microservices, led platform architecture
    """
    
    sample_jd = """
    Senior Backend Engineer
    Requirements: 5+ years backend development, Kubernetes, AWS, microservices
    """
    
    # Run analysis with HF/vLLM
    result = run_analysis_crew_hf(sample_resume, sample_jd, use_reasoning=True)
    print("\nAnalysis Result:")
    print(result)
