"""
HuggingFace vLLM Configuration Module for NaukriAgent.
Sets up HF models with vLLM inference engine.

Model: Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled
- Base: Qwen3.5-27B (27B parameters)
- Reasoning: Claude-4.6-Opus-style distilled reasoning
- Capabilities: Strong analytical reasoning, coding, math, logic
- Memory: ~16.5 GB VRAM with Q4_K_M quantization
- Speed: 29-35 tokens/sec generation
- Context: 262K context window
"""

import os
from typing import Optional
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- HF MODEL CONFIGURATION ---
# Model path or HF repo ID
HF_MODEL_ID = os.getenv(
    "HF_MODEL_ID",
    "Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled"
)

# vLLM server configuration
VLLM_BASE_URL = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
VLLM_API_KEY = os.getenv("VLLM_API_KEY", "not-needed")

# Model-specific parameters
HF_QUANTIZATION = os.getenv("HF_QUANTIZATION", "auto")  # auto, awq, gptq, int8
HF_DTYPE = os.getenv("HF_DTYPE", "bfloat16")  # float16, bfloat16, float32
VLLM_TENSOR_PARALLEL_SIZE = int(os.getenv("VLLM_TENSOR_PARALLEL_SIZE", "1"))
VLLM_GPU_MEMORY_UTILIZATION = float(
    os.getenv("VLLM_GPU_MEMORY_UTILIZATION", "0.9")
)

# Generation parameters
MAX_TOKENS = int(os.getenv("HF_MAX_TOKENS", "2000"))
TEMPERATURE = float(os.getenv("HF_TEMPERATURE", "0.7"))
TOP_P = float(os.getenv("HF_TOP_P", "0.95"))
TOP_K = int(os.getenv("HF_TOP_K", "40"))

# Reasoning-specific parameters for Qwen3.5-Opus
THINKING_ENABLED = os.getenv("THINKING_ENABLED", "true").lower() == "true"
THINKING_MAX_TOKENS = int(os.getenv("THINKING_MAX_TOKENS", "8000"))


def get_hf_slm(model_id: Optional[str] = None):
    """
    Initialize and return the HuggingFace-based SLM using vLLM inference.
    
    Args:
        model_id (str, optional): HuggingFace model ID or path.
                                 Defaults to Qwen3.5-Claude-Opus.
    
    Returns:
        ChatOpenAI: Configured language model instance compatible with CrewAI.
    
    Raises:
        ConnectionError: If unable to connect to vLLM server.
        ValueError: If model_id is invalid.
    
    Example:
        >>> slm = get_hf_slm()
        >>> response = slm.invoke("Analyze this resume...")
    """
    if model_id is None:
        model_id = HF_MODEL_ID
    
    try:
        # Initialize ChatOpenAI with vLLM backend
        slm = ChatOpenAI(
            model=model_id,
            base_url=VLLM_BASE_URL,
            api_key=VLLM_API_KEY,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            top_p=TOP_P,
            top_k=TOP_K,
            # vLLM-specific parameters
            extra_body={
                "dtype": HF_DTYPE,
                "quantization": HF_QUANTIZATION,
            }
        )
        
        print(f"✓ HuggingFace SLM initialized")
        print(f"  Model: {model_id}")
        print(f"  vLLM Server: {VLLM_BASE_URL}")
        print(f"  Dtype: {HF_DTYPE}")
        print(f"  Temperature: {TEMPERATURE}")
        
        return slm
        
    except ConnectionError as e:
        raise ConnectionError(
            f"Failed to connect to vLLM server at {VLLM_BASE_URL}. "
            f"Ensure vLLM is running with: "
            f"python -m vllm.entrypoints.openai.api_server "
            f"--model {model_id} "
            f"--dtype {HF_DTYPE} "
            f"--tensor-parallel-size {VLLM_TENSOR_PARALLEL_SIZE} "
            f"--gpu-memory-utilization {VLLM_GPU_MEMORY_UTILIZATION} "
            f"Error: {e}"
        )
    except ValueError as e:
        raise ValueError(
            f"Invalid model configuration. "
            f"Model ID: {model_id}, "
            f"Error: {e}"
        )
    except Exception as e:
        raise Exception(
            f"Failed to initialize HuggingFace SLM: {e}"
        )


def get_hf_slm_with_reasoning(model_id: Optional[str] = None):
    """
    Initialize HuggingFace SLM with reasoning-specific optimizations.
    
    This is optimized for the Qwen3.5-Claude-Opus-Reasoning model,
    which uses structured <think>...</think> reasoning blocks.
    
    Args:
        model_id (str, optional): HuggingFace model ID.
    
    Returns:
        ChatOpenAI: Configured model with reasoning optimizations.
    """
    if model_id is None:
        model_id = HF_MODEL_ID
    
    # Reasoning-optimized parameters
    reasoning_params = {
        "temperature": max(0.7, TEMPERATURE),  # Slightly higher for more reasoning
        "top_p": min(0.95, TOP_P),
        "max_tokens": MAX_TOKENS,
        "extra_body": {
            "dtype": HF_DTYPE,
            "quantization": HF_QUANTIZATION,
            "thinking_enabled": THINKING_ENABLED,
            "thinking_max_tokens": THINKING_MAX_TOKENS,
        }
    }
    
    try:
        slm = ChatOpenAI(
            model=model_id,
            base_url=VLLM_BASE_URL,
            api_key=VLLM_API_KEY,
            **reasoning_params
        )
        
        print(f"✓ HuggingFace SLM with Reasoning initialized")
        print(f"  Model: {model_id}")
        print(f"  Thinking Mode: {'Enabled' if THINKING_ENABLED else 'Disabled'}")
        print(f"  Thinking Max Tokens: {THINKING_MAX_TOKENS}")
        
        return slm
        
    except Exception as e:
        raise Exception(f"Failed to initialize reasoning SLM: {e}")


# --- VLLM STARTUP HELPER ---
def print_vllm_startup_command():
    """
    Print the vLLM startup command for the configured model.
    Useful for documentation and quick copy-paste.
    """
    command = f"""
# vLLM Startup Command for Qwen3.5-Claude-Opus-Reasoning-Distilled

python -m vllm.entrypoints.openai.api_server \\
    --model {HF_MODEL_ID} \\
    --dtype {HF_DTYPE} \\
    --quantization {HF_QUANTIZATION} \\
    --tensor-parallel-size {VLLM_TENSOR_PARALLEL_SIZE} \\
    --gpu-memory-utilization {VLLM_GPU_MEMORY_UTILIZATION} \\
    --port 8000 \\
    --api-key {VLLM_API_KEY}

# Or for Q4 quantization (lower memory):
python -m vllm.entrypoints.openai.api_server \\
    --model {HF_MODEL_ID} \\
    --dtype float16 \\
    --quantization awq \\
    --tensor-parallel-size 1 \\
    --gpu-memory-utilization 0.85 \\
    --port 8000
"""
    return command


# --- MODEL INFORMATION ---
MODEL_INFO = {
    "name": "Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled",
    "base_model": "Qwen3.5-27B",
    "parameters": "27B",
    "reasoning_type": "Claude-4.6-Opus-Distilled",
    "capabilities": [
        "Analytical reasoning",
        "Code generation",
        "Mathematical problem-solving",
        "Logic-based reasoning",
        "Tool calling",
        "Multi-turn conversations"
    ],
    "memory_requirements": {
        "full_precision": "~60 GB VRAM (bfloat16)",
        "awq_quantization": "~16-20 GB VRAM",
        "gptq_quantization": "~14-16 GB VRAM"
    },
    "inference_speed": "29-35 tokens/sec (single GPU)",
    "context_length": 262144,  # 262K tokens
    "supported_quantizations": ["int8", "float16", "bfloat16", "awq", "gptq"],
    "special_features": [
        "Structured thinking with <think>...</think> tags",
        "Efficient reasoning (reduced redundant loops)",
        "Native developer role support",
        "Extended 262K context window",
        "Chain-of-thought reasoning"
    ],
    "huggingface_url": "https://huggingface.co/Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled"
}


def print_model_info():
    """Print detailed model information."""
    print("\n" + "=" * 70)
    print(f"Model: {MODEL_INFO['name']}")
    print(f"Base: {MODEL_INFO['base_model']} ({MODEL_INFO['parameters']})")
    print(f"Reasoning: {MODEL_INFO['reasoning_type']}")
    print("=" * 70)
    
    print("\nCapabilities:")
    for cap in MODEL_INFO['capabilities']:
        print(f"  • {cap}")
    
    print("\nMemory Requirements:")
    for precision, mem in MODEL_INFO['memory_requirements'].items():
        print(f"  • {precision}: {mem}")
    
    print(f"\nInference Speed: {MODEL_INFO['inference_speed']}")
    print(f"Context Length: {MODEL_INFO['context_length']:,} tokens")
    
    print("\nSpecial Features:")
    for feature in MODEL_INFO['special_features']:
        print(f"  ✓ {feature}")
    
    print("\n" + "=" * 70)


# --- ENVIRONMENT VARIABLE REFERENCE ---
"""
Environment Variables for config_hf.py:

# Model Configuration
HF_MODEL_ID=Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled
VLLM_BASE_URL=http://localhost:8000/v1
VLLM_API_KEY=not-needed

# Quantization (auto, awq, gptq, int8)
HF_QUANTIZATION=auto

# Data type (float16, bfloat16, float32)
HF_DTYPE=bfloat16

# Parallel inference
VLLM_TENSOR_PARALLEL_SIZE=1

# GPU memory usage (0.0-1.0)
VLLM_GPU_MEMORY_UTILIZATION=0.9

# Generation parameters
HF_MAX_TOKENS=2000
HF_TEMPERATURE=0.7
HF_TOP_P=0.95
HF_TOP_K=40

# Reasoning mode
THINKING_ENABLED=true
THINKING_MAX_TOKENS=8000
"""


if __name__ == "__main__":
    # Display model info and startup command
    print_model_info()
    print("\n" + print_vllm_startup_command())
