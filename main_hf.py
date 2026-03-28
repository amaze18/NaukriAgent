#!/usr/bin/env python3
"""
Main entry point for NaukriAgent using HuggingFace vLLM inference.

Uses: Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled
Backend: vLLM (OpenAI-compatible API)

This is an alternative to main.py that uses HuggingFace models
instead of local Ollama models, with support for reasoning chains.
"""

from workflow_hf import get_compiled_app_hf
from state import AgentState


def create_sample_input() -> dict:
    """
    Create sample resume and JD for testing HF inference.
    
    Returns:
        dict: Sample input data matching AgentState structure.
    """
    resume = """
    Sarah Chen
    Email: sarah.chen@email.com
    Phone: +1-555-987-6543
    
    PROFESSIONAL SUMMARY
    Senior Software Engineer with 7+ years of experience in cloud-native 
    architecture, machine learning systems, and full-stack development. 
    Expertise in Python, Rust, and Go with demonstrated leadership in 
    building high-performance distributed systems.
    
    TECHNICAL SKILLS
    Languages: Python, Rust, Go, TypeScript, C++
    Frameworks: FastAPI, Actix-web, Django, FastAPI
    ML/AI: PyTorch, TensorFlow, scikit-learn, Hugging Face
    Cloud: AWS (S3, EC2, Lambda, RDS), GCP (Compute Engine, BigQuery), Azure
    DevOps: Docker, Kubernetes, Terraform, GitHub Actions, GitLab CI
    Databases: PostgreSQL, MongoDB, Redis, Elasticsearch
    Architectures: Microservices, Event-driven, Distributed systems
    
    PROFESSIONAL EXPERIENCE
    
    Senior Software Engineer | CloudTech Solutions | 2021-Present
    - Architected and led development of real-time ML inference platform
    - Designed microservices using Kubernetes, reducing latency by 60%
    - Implemented ML model serving with 99.9% uptime SLA
    - Mentored 5 junior engineers and conducted technical interviews
    - Published 2 technical papers on distributed ML systems
    
    Software Engineer | DataFlow Inc. | 2018-2021
    - Built data pipeline processing 10TB+ daily using Python and Spark
    - Optimized database queries, improving performance by 3x
    - Implemented CI/CD pipelines using GitHub Actions
    - Collaborated with data scientists on feature engineering
    
    Junior Developer | StartupAI | 2017-2018
    - Developed Python backend services for ML model management
    - Implemented REST APIs using Django and FastAPI
    - Created automated testing suite (90% coverage)
    
    EDUCATION
    M.S. Computer Science, Focus on Distributed Systems
    Tech University, Graduated 2017
    GPA: 3.8/4.0
    
    B.S. Computer Science with Minor in Statistics
    State College, Graduated 2015
    
    CERTIFICATIONS
    - AWS Certified Solutions Architect Professional
    - Certified Kubernetes Administrator (CKA)
    - Deep Learning Specialization (Coursera)
    
    PROJECTS & PUBLICATIONS
    - Open Source: Core contributor to popular Python ML library (2.5K stars)
    - Published: "Efficient ML Model Serving at Scale" (Conference 2023)
    - Project: Built autonomous trading system using deep learning (personal)
    """
    
    jd = """
    JOB POSTING: Senior Machine Learning Engineer
    Company: FinTech Innovation Labs
    Location: Remote (US/EU timezone preferred)
    
    POSITION OVERVIEW
    We are seeking a Senior Machine Learning Engineer to lead the development 
    of next-generation ML systems for financial services. You will architect 
    scalable ML pipelines and mentor a team of engineers.
    
    REQUIRED QUALIFICATIONS
    - 6+ years of professional experience in software engineering
    - 3+ years of experience building and deploying ML systems in production
    - Strong proficiency in Python
    - Deep understanding of distributed systems and microservices
    - Experience with containerization (Docker, Kubernetes)
    - Master's degree in Computer Science or related field (or equivalent)
    - Experience deploying ML models with high availability requirements
    - Excellent communication and team collaboration skills
    
    REQUIRED SKILLS
    - ML Frameworks: PyTorch, TensorFlow, or scikit-learn
    - Cloud Platforms: AWS or GCP (hands-on experience)
    - System Design: Understanding of scalable architectures
    - Backend Development: RESTful APIs, microservices
    - Data Engineering: Data pipelines, ETL concepts
    
    NICE-TO-HAVE QUALIFICATIONS
    - Experience with Kubernetes for ML workloads
    - Published research or technical blog posts
    - Open source contributions
    - Rust or Go experience for performance-critical systems
    - Experience with feature stores or ML ops platforms
    - Fintech/trading systems experience
    
    RESPONSIBILITIES
    - Design and implement scalable ML inference pipelines
    - Lead technical architecture decisions for ML platform
    - Mentor junior engineers and conduct code reviews
    - Collaborate with data scientists on model optimization
    - Ensure production systems maintain 99.9%+ uptime
    - Participate in system design and architecture discussions
    - Contribute to technical documentation and knowledge sharing
    
    WHAT WE OFFER
    - Competitive salary ($180K-$250K based on experience)
    - Stock options with 4-year vest
    - Comprehensive health/dental/vision insurance
    - Remote work flexibility
    - $15K annual learning/conference budget
    - Collaborative team with 8+ ML engineers
    - Cutting-edge ML infrastructure
    
    INTERVIEW PROCESS
    1. Initial screening (30 min)
    2. Technical phone screen with ML focus (60 min)
    3. System design interview (90 min)
    4. Team fit interview with engineers (60 min)
    5. Offer discussion
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
        "candidate_name": "Sarah Chen",
        "candidate_email": "sarah.chen@email.com"
    }


def run_workflow_hf(inputs: dict = None):
    """
    Execute the NaukriAgent workflow using HuggingFace inference.
    
    Args:
        inputs (dict, optional): Input data. If None, uses sample data.
    
    Raises:
        Exception: If workflow execution fails.
    """
    if inputs is None:
        inputs = create_sample_input()
    
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "NAUKRIAGENT (HuggingFace vLLM)" + " " * 20 + "║")
    print("║" + " " * 14 + "Qwen3.5-Claude-Opus Reasoning" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    
    try:
        # Get compiled HF workflow
        app = get_compiled_app_hf()
        
        print("\n✓ HuggingFace LangGraph workflow initialized")
        print(f"  Model: Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled")
        print(f"  Candidate: {inputs['candidate_name']}")
        print("\nExecuting workflow...")
        print("-" * 60)
        
        final_state = None
        step_count = 0
        
        # Stream workflow execution
        for output in app.stream(inputs):
            step_count += 1
            node_name = list(output.keys())[0]
            node_output = output[node_name]
            final_state = node_output
        
        # Print final results
        print("\n" + "=" * 60)
        print("WORKFLOW COMPLETED (HuggingFace Inference)")
        print("=" * 60)
        
        print(f"\nCandidate: {final_state['candidate_name']}")
        print(f"Email: {final_state['candidate_email']}")
        print(f"Overall Score: {final_state['overall_score']}%")
        print(f"Skill Match: {final_state['skill_match_score']:.0f}%")
        print(f"Experience Match: {final_state['experience_match_score']:.0f}%")
        print(f"\nFinal Status: {final_state['status'].upper()}")
        
        if final_state['status'] == 'approved':
            print("\n✓ CANDIDATE APPROVED AND SHORTLISTED")
            print("Action: Send offer letter and schedule onboarding")
        elif final_state['status'] == 'rejected':
            reason = final_state.get('rejection_reason', 'Did not meet requirements')
            print(f"\n✗ CANDIDATE REJECTED")
            print(f"Reason: {reason}")
        else:
            print("\n⊘ PENDING - Requires manual review")
        
        if final_state.get('recruiter_notes'):
            print(f"\nRecruiter Notes:\n{final_state['recruiter_notes']}")
        
        print("\n" + "=" * 60)
        print(f"Analysis Method: Qwen3.5-Claude-Opus reasoning chains")
        print(f"Reasoning Quality: High (structured <think> blocks)")
        print("=" * 60 + "\n")
        
        return final_state
        
    except KeyboardInterrupt:
        print("\n\n⊘ Workflow interrupted by user")
        return None
    except ConnectionError as e:
        print(f"\n✗ Connection Error: {e}")
        print("\nEnsure vLLM server is running:")
        print("  python -m vllm.entrypoints.openai.api_server \\")
        print("      --model Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled \\")
        print("      --port 8000")
        raise
    except Exception as e:
        print(f"\n✗ Workflow failed: {e}")
        raise


def run_custom_workflow_hf(resume: str, jd: str, candidate_name: str = "Unknown",
                          candidate_email: str = ""):
    """
    Run workflow with custom resume and JD using HF inference.
    
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
    
    return run_workflow_hf(inputs)


def compare_workflows():
    """
    Run workflow with both standard and HF models for comparison.
    Useful for evaluating reasoning quality.
    """
    print("\n" + "=" * 70)
    print("COMPARISON: Standard Ollama vs HuggingFace vLLM")
    print("=" * 70)
    
    inputs = create_sample_input()
    
    print("\n[1/2] Running with HuggingFace vLLM...")
    result_hf = run_workflow_hf(inputs)
    
    print("\n[2/2] Running with Ollama...")
    # Import and run standard workflow
    from main import run_workflow
    result_ollama = run_workflow(inputs)
    
    # Compare results
    print("\n" + "=" * 70)
    print("COMPARISON RESULTS")
    print("=" * 70)
    print(f"HF Score: {result_hf['overall_score']}%")
    print(f"Ollama Score: {result_ollama['overall_score']}%")
    print(f"Difference: {abs(result_hf['overall_score'] - result_ollama['overall_score'])}%")


if __name__ == "__main__":
    # Run with sample data using HuggingFace vLLM
    final_state = run_workflow_hf()
    
    # To run with custom data:
    # my_resume = "..."
    # my_jd = "..."
    # final_state = run_custom_workflow_hf(my_resume, my_jd, "Name", "email@example.com")
    
    # To compare standard and HF workflows:
    # compare_workflows()
