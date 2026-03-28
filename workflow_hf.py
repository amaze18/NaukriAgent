"""
LangGraph workflow for HuggingFace vLLM inference.
Identical workflow structure to workflow.py but uses HF-based nodes.

Uses Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled via vLLM backend.
"""

from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes_hf import (
    validate_inputs_hf,
    run_crew_analysis_hf,
    scoring_engine_hf,
    human_approval_hf,
    generate_shortlist_hf
)


def build_workflow_hf():
    """
    Build the LangGraph workflow for HuggingFace inference.
    
    Same 6-node architecture but with HuggingFace-optimized nodes:
    
    Workflow Nodes:
        1. validate_inputs_hf: Validate resume and JD
        2. run_crew_analysis_hf: CrewAI with HF vLLM (Nodes 2 & 3)
        3. scoring_engine_hf: Calculate scores from HF analysis (Node 4)
        4. human_approval_hf: Recruiter approval gate (Node 5)
        5. generate_shortlist_hf: Finalize decision (Node 6)
    
    Returns:
        Compiled LangGraph workflow application.
    """
    
    workflow = StateGraph(AgentState)
    
    # Add all nodes
    workflow.add_node("validate", validate_inputs_hf)
    workflow.add_node("crew_analysis", run_crew_analysis_hf)
    workflow.add_node("scoring", scoring_engine_hf)
    workflow.add_node("approval", human_approval_hf)
    workflow.add_node("finalize", generate_shortlist_hf)
    
    # Define edges
    workflow.add_edge(START, "validate")
    workflow.add_edge("validate", "crew_analysis")
    workflow.add_edge("crew_analysis", "scoring")
    workflow.add_edge("scoring", "approval")
    
    # Conditional edge: Approval decision
    def route_decision(state: AgentState):
        """Route based on recruiter approval."""
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
    
    # Compile
    app = workflow.compile()
    
    return app


def get_compiled_app_hf():
    """
    Get the compiled HuggingFace LangGraph application.
    
    Returns:
        Compiled LangGraph workflow app with HF inference.
    """
    return build_workflow_hf()


# --- UTILITY FUNCTIONS ---

def print_workflow_info():
    """Print information about the HF workflow."""
    info = """
╔════════════════════════════════════════════════════════════════╗
║    NaukriAgent - HuggingFace vLLM Workflow                   ║
╚════════════════════════════════════════════════════════════════╝

Model: Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled
Backend: vLLM (OpenAI-compatible API)
Server: http://localhost:8000/v1

Workflow Architecture:
  ├─ Node 1: validate_inputs_hf
  │   └─ Validate resume and JD
  │
  ├─ Nodes 2-3: run_crew_analysis_hf
  │   ├─ Resume Analyzer (HF/vLLM)
  │   ├─ JD Matcher (HF/vLLM)
  │   └─ Skill Assessor (optional, HF/vLLM)
  │
  ├─ Node 4: scoring_engine_hf
  │   ├─ Calculate skill match (60% weight)
  │   ├─ Calculate experience match (40% weight)
  │   └─ Apply reasoning confidence adjustments
  │
  ├─ Node 5: human_approval_hf
  │   ├─ Display HF analysis
  │   ├─ Get recruiter decision
  │   └─ Route: Approve → Node 6 | Reject → END
  │
  └─ Node 6: generate_shortlist_hf
      └─ Finalize and notify

Key Advantages:
  ✓ Claude-4.6-Opus reasoning distilled to 27B model
  ✓ Structured thinking with <think> tags
  ✓ 262K context window
  ✓ 29-35 tokens/sec generation speed
  ✓ Tool calling support
  ✓ Efficient reasoning (no redundant loops)
"""
    print(info)


def print_vllm_setup_guide():
    """Print setup guide for vLLM with Qwen3.5 model."""
    guide = """
╔════════════════════════════════════════════════════════════════╗
║  vLLM Setup Guide for Qwen3.5-Claude-Opus                   ║
╚════════════════════════════════════════════════════════════════╝

1. Install vLLM and dependencies:
   
   pip install vllm
   pip install huggingface-hub

2. Verify model access:
   
   # Login to Hugging Face (if model requires it)
   huggingface-cli login
   
   # Pre-download model (optional)
   huggingface-cli download Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled

3. Start vLLM server:
   
   # Full precision (requires ~60GB VRAM)
   python -m vllm.entrypoints.openai.api_server \\
       --model Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled \\
       --dtype bfloat16 \\
       --tensor-parallel-size 1 \\
       --gpu-memory-utilization 0.9 \\
       --port 8000
   
   # With AWQ Quantization (requires ~16-20GB VRAM)
   python -m vllm.entrypoints.openai.api_server \\
       --model Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled \\
       --dtype float16 \\
       --quantization awq \\
       --tensor-parallel-size 1 \\
       --gpu-memory-utilization 0.85 \\
       --port 8000
   
   # Multi-GPU setup (for very large models)
   python -m vllm.entrypoints.openai.api_server \\
       --model Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled \\
       --dtype bfloat16 \\
       --tensor-parallel-size 2 \\
       --gpu-memory-utilization 0.9 \\
       --port 8000

4. Test the server:
   
   # In another terminal
   curl http://localhost:8000/v1/models
   
   # Should return model information

5. Configure NaukriAgent:
   
   # Update .env
   HF_MODEL_ID=Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled
   VLLM_BASE_URL=http://localhost:8000/v1
   HF_DTYPE=bfloat16
   THINKING_ENABLED=true

6. Run NaukriAgent with HF workflow:
   
   # Use main_hf.py instead of main.py
   python main_hf.py

Common Issues:
  - "Connection refused": Ensure vLLM server is running
  - OOM errors: Use quantization (awq/gptq) or reduce batch size
  - Slow inference: Check GPU utilization with nvidia-smi
"""
    print(guide)


if __name__ == "__main__":
    print_workflow_info()
    print("\n" + "=" * 70 + "\n")
    print_vllm_setup_guide()
