#!/usr/bin/env python3
"""
Main entry point for NaukriAgent.
Demonstrates how to run the LangGraph workflow with sample data.
"""

import json
from workflow import get_compiled_app
from state import AgentState


def create_sample_input() -> dict:
    """
    Create sample resume and JD for testing.
    
    Returns:
        dict: Sample input data matching AgentState structure.
    """
    resume = """
    John Doe
    Email: john.doe@email.com
    Phone: +1-555-123-4567
    
    PROFESSIONAL SUMMARY
    Senior Software Engineer with 5+ years of experience in Python development,
    cloud architectures, and full-stack web applications. Proven track record in
    building scalable systems and leading technical teams.
    
    TECHNICAL SKILLS
    Languages: Python, JavaScript, TypeScript, SQL, Go
    Frameworks: Django, FastAPI, React, Next.js
    Cloud: AWS (EC2, S3, Lambda), Google Cloud Platform, Azure
    Tools: Docker, Kubernetes, Git, CI/CD (GitHub Actions, Jenkins)
    Databases: PostgreSQL, MongoDB, Redis
    
    PROFESSIONAL EXPERIENCE
    
    Senior Software Engineer | TechCorp Inc. | 2022-Present
    - Led development of microservices architecture using Python and FastAPI
    - Designed and implemented automated testing pipelines (90% code coverage)
    - Mentored junior developers and conducted code reviews
    - Reduced API response time by 40% through optimization
    
    Software Engineer | StartupXYZ | 2020-2022
    - Developed full-stack web applications using Django and React
    - Implemented cloud migration strategy to AWS (saved 30% infrastructure costs)
    - Created comprehensive API documentation using OpenAPI/Swagger
    
    Junior Developer | DevShop LLC | 2019-2020
    - Built Python scripts for data processing and automation
    - Collaborated with cross-functional teams on feature development
    
    EDUCATION
    Bachelor of Science in Computer Science
    State University, Graduated 2019
    
    CERTIFICATIONS
    - AWS Certified Solutions Architect Associate
    - Certified Kubernetes Administrator (CKA)
    
    PROJECTS
    - Personal Project: Built an ML recommendation engine using Python (scikit-learn)
    - Open Source: Contributed to popular Python web framework
    """
    
    jd = """
    Job Title: Senior Python Developer
    Company: FinTech Innovations Ltd.
    
    JOB DESCRIPTION
    We are looking for an experienced Senior Python Developer to join our growing team.
    
    REQUIREMENTS
    Required Skills:
    - 4+ years of professional Python development experience
    - Strong understanding of RESTful API design
    - Experience with cloud platforms (AWS, GCP, or Azure)
    - Proficiency in SQL and NoSQL databases
    - Knowledge of microservices architecture
    - Experience with Docker and containerization
    - Excellent problem-solving and communication skills
    
    Nice-to-Have:
    - Experience with FastAPI or similar async frameworks
    - Kubernetes experience
    - CI/CD pipeline implementation
    - Open source contributions
    - AWS certifications
    
    RESPONSIBILITIES
    - Design and develop scalable Python applications
    - Collaborate with product and design teams
    - Write clean, maintainable code with comprehensive tests
    - Participate in code reviews and technical discussions
    - Contribute to system architecture decisions
    - Mentor junior developers
    
    BENEFITS
    - Competitive salary package
    - Remote work options
    - Professional development opportunities
    - Stock options
    """
    
    return {
        "resume": resume,
        "jd": jd,
        "analysis_results": "",
        "skill_match_score": 0.0,
        "experience_match_score": 0.0,
        "overall_score": 0,
        "status": "pending",
        "rejection_reason": "",
        "recruiter_notes": "",
        "candidate_name": "John Doe",
        "candidate_email": "john.doe@email.com"
    }


def run_workflow(inputs: dict = None):
    """
    Execute the NaukriAgent workflow.
    
    Args:
        inputs (dict, optional): Input data for the workflow.
                                If None, uses sample data.
    
    Raises:
        Exception: If workflow execution fails.
    """
    # Use sample data if not provided
    if inputs is None:
        inputs = create_sample_input()
    
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "NAUKRIAGENT WORKFLOW START" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")
    
    try:
        # Get the compiled workflow
        app = get_compiled_app()
        
        # Execute the workflow
        print("\nExecuting workflow...")
        print("-" * 60)
        
        final_state = None
        for output in app.stream(inputs):
            # Each output is a dict with node name as key
            node_name = list(output.keys())[0]
            node_output = output[node_name]
            final_state = node_output
            
            # Update status and continue
        
        # Print final results
        print("\n" + "=" * 60)
        print("WORKFLOW COMPLETED")
        print("=" * 60)
        
        print(f"\nFinal Candidate Status: {final_state['status'].upper()}")
        print(f"Overall Score: {final_state['overall_score']}%")
        print(f"Candidate: {final_state['candidate_name']}")
        print(f"Email: {final_state['candidate_email']}")
        
        if final_state['status'] == 'approved':
            print("\n✓ CANDIDATE APPROVED AND SHORTLISTED")
        elif final_state['status'] == 'rejected':
            print(f"\n✗ CANDIDATE REJECTED")
            if final_state.get('rejection_reason'):
                print(f"   Reason: {final_state['rejection_reason']}")
        else:
            print("\n⊘ PENDING - Requires manual review")
        
        print("\n" + "=" * 60)
        
        return final_state
        
    except KeyboardInterrupt:
        print("\n\n⊘ Workflow interrupted by user")
        return None
    except Exception as e:
        print(f"\n✗ Workflow failed with error: {e}")
        raise


def run_custom_workflow(resume: str, jd: str, candidate_name: str = "Unknown", 
                       candidate_email: str = ""):
    """
    Run workflow with custom resume and JD.
    
    Args:
        resume (str): Candidate's resume content.
        jd (str): Job description content.
        candidate_name (str): Name of the candidate.
        candidate_email (str): Email of the candidate.
    
    Returns:
        dict: Final workflow state.
    """
    inputs = {
        "resume": resume,
        "jd": jd,
        "analysis_results": "",
        "skill_match_score": 0.0,
        "experience_match_score": 0.0,
        "overall_score": 0,
        "status": "pending",
        "rejection_reason": "",
        "recruiter_notes": "",
        "candidate_name": candidate_name,
        "candidate_email": candidate_email
    }
    
    return run_workflow(inputs)


if __name__ == "__main__":
    # Run with sample data
    final_state = run_workflow()
    
    # To run with custom data, uncomment and modify:
    # my_resume = "..."
    # my_jd = "..."
    # final_state = run_custom_workflow(my_resume, my_jd, "Candidate Name", "email@example.com")
