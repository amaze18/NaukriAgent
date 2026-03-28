# HuggingFace vLLM Integration Guide

## Overview

This guide explains how to use **NaukriAgent** with **HuggingFace models** via **vLLM** backend, specifically the **Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled** model.

### Why HuggingFace Models?

- **Reasoning Chains**: Built-in `<think>...</think>` reasoning blocks for transparent AI decision-making
- **Open Source**: Full model control and no API rate limits
- **Cost Effective**: One-time hardware investment vs. ongoing API costs
- **Privacy**: Run locally without sending data to external APIs
- **Performance**: 29-35 tokens/sec on modern GPUs
- **Large Context**: 262K context window for complex document analysis
- **Distilled Knowledge**: Claude-4.6-Opus reasoning distilled into 27B parameters

---

## Quick Start (5 Minutes)

### Step 1: Install vLLM

```bash
pip install vllm
pip install huggingface-hub
```

### Step 2: Start vLLM Server

```bash
python -m vllm.entrypoints.openai.api_server \
    --model Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled \
    --dtype bfloat16 \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.9 \
    --port 8000
```

### Step 3: Configure NaukriAgent

Update `.env`:

```env
HF_MODEL_ID=Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled
VLLM_BASE_URL=http://localhost:8000/v1
HF_DTYPE=bfloat16
THINKING_ENABLED=true
```

### Step 4: Run HF Workflow

```bash
python main_hf.py
```

---

## File Structure

### HuggingFace-Specific Files

```
NaukriAgent/
├── config_hf.py           # HF/vLLM configuration
├── agents_hf.py           # CrewAI with HF models
├── nodes_hf.py            # Workflow nodes for HF
├── workflow_hf.py         # LangGraph with HF
├── main_hf.py             # Entry point for HF workflow
└── HF_SETUP_GUIDE.md      # This file
```

### Using HF Components

| File | Purpose | Replace With |
|------|---------|--------------|
| **config_hf.py** | HF/vLLM config | config.py (Ollama) |
| **agents_hf.py** | HF agents | agents.py (Ollama) |
| **nodes_hf.py** | HF nodes | nodes.py (Ollama) |
| **workflow_hf.py** | HF workflow | workflow.py (Ollama) |
| **main_hf.py** | HF entry | main.py (Ollama) |

---

## Installation & Setup

### Prerequisites

- **CUDA 12.1+** (for GPU inference)
- **8GB+ VRAM** (minimum for quantized model)
- **Python 3.10+**
- **HuggingFace account** (free, for model access)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install vllm torch accelerate
```

### 2. Login to HuggingFace (Optional)

```bash
huggingface-cli login
# Enter your HF token when prompted
```

### 3. Pre-download Model (Optional)

```bash
# This downloads the full model ~56GB
huggingface-cli download \
    Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled
```

### 4. Start vLLM Server

Choose based on your GPU VRAM:

#### Option A: Full Precision (60GB VRAM needed)

```bash
python -m vllm.entrypoints.openai.api_server \
    --model Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled \
    --dtype bfloat16 \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.9 \
    --port 8000 \
    --api-key not-needed
```

#### Option B: AWQ Quantization (16-20GB VRAM)

```bash
python -m vllm.entrypoints.openai.api_server \
    --model Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled \
    --dtype float16 \
    --quantization awq \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.85 \
    --port 8000 \
    --api-key not-needed
```

#### Option C: GPTQ Quantization (14-16GB VRAM)

```bash
python -m vllm.entrypoints.openai.api_server \
    --model Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled \
    --dtype float16 \
    --quantization gptq \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.8 \
    --port 8000 \
    --api-key not-needed
```

#### Option D: Multi-GPU (for distributed inference)

```bash
python -m vllm.entrypoints.openai.api_server \
    --model Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled \
    --dtype bfloat16 \
    --tensor-parallel-size 2 \
    --gpu-memory-utilization 0.9 \
    --port 8000 \
    --api-key not-needed
```

### 5. Configure NaukriAgent

Create `.env` file:

```env
# HuggingFace Configuration
HF_MODEL_ID=Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled
VLLM_BASE_URL=http://localhost:8000/v1
VLLM_API_KEY=not-needed
HF_DTYPE=bfloat16
HF_QUANTIZATION=auto

# Reasoning Configuration
THINKING_ENABLED=true
THINKING_MAX_TOKENS=8000

# Generation Parameters
HF_MAX_TOKENS=2000
HF_TEMPERATURE=0.7
HF_TOP_P=0.95
HF_TOP_K=40

# Application
DEFAULT_SCORE_THRESHOLD=75
APPROVAL_REQUIRED=true
```

### 6. Run NaukriAgent

```bash
# In a new terminal (vLLM server should be running in another)
python main_hf.py
```

---

## Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HF_MODEL_ID` | Jackrong/... | HuggingFace model ID |
| `VLLM_BASE_URL` | http://localhost:8000/v1 | vLLM server URL |
| `VLLM_API_KEY` | not-needed | API key for vLLM |
| `HF_DTYPE` | bfloat16 | Data type (float16, bfloat16) |
| `HF_QUANTIZATION` | auto | Quantization (auto, awq, gptq) |
| `HF_MAX_TOKENS` | 2000 | Max generation tokens |
| `HF_TEMPERATURE` | 0.7 | Generation temperature |
| `HF_TOP_P` | 0.95 | Top-p sampling |
| `HF_TOP_K` | 40 | Top-k sampling |
| `THINKING_ENABLED` | true | Enable reasoning chains |
| `THINKING_MAX_TOKENS` | 8000 | Max thinking tokens |

### Customizing Weights

Edit `nodes_hf.py` `scoring_engine_hf()`:

```python
# Adjust weights
overall_score = int(
    (skill_score * 0.6) +        # Increase for more emphasis on skills
    (experience_score * 0.4)     # Adjust for experience
)
```

---

## Advanced Usage

### 1. Using Reasoning Mode

Qwen3.5 includes structured reasoning. Enable it in `config_hf.py`:

```python
slm = get_hf_slm_with_reasoning()
```

This uses:
- `<think>...</think>` blocks for internal reasoning
- Structured problem-solving approach
- Transparent chain-of-thought reasoning

### 2. Adding Custom Agents

Edit `agents_hf.py`:

```python
def get_cultural_fit_assessor(slm):
    return Agent(
        role='Cultural Fit Assessor',
        goal='Assess candidate culture and team fit',
        llm=slm
    )
```

Add to crew:

```python
agents = [analyzer, matcher, cultural_assessor]
tasks = [analyze_task, match_task, culture_task]
```

### 3. Analyzing Reasoning Chains

Use `nodes_hf.py` `analyze_reasoning_chain()`:

```python
from nodes_hf import analyze_reasoning_chain

reasoning_info = analyze_reasoning_chain(final_state)
print(f"Thinking blocks: {reasoning_info['thinking_blocks']}")
print(f"Reasoning quality: {reasoning_info['reasoning_present']}")
```

### 4. Comparing Models

Run both standard and HF workflows:

```python
from main_hf import compare_workflows
compare_workflows()
```

---

## Performance Optimization

### Memory Optimization

1. **Use Quantization**: Reduces VRAM by 50-70%
   ```bash
   --quantization awq  # ~16-20GB VRAM
   ```

2. **Batch Processing**: Process multiple candidates in parallel
   ```python
   # Add batching logic in main_hf.py
   ```

3. **Context Pruning**: Reduce input size for faster processing
   ```python
   resume = resume[:8000]  # Limit to 8K chars
   ```

### Speed Optimization

1. **Enable Caching**: vLLM automatically caches KV values
2. **Use Tensor Parallelism**: For multi-GPU systems
   ```bash
   --tensor-parallel-size 2
   ```
3. **Adjust Generation Parameters**:
   ```env
   HF_TOP_P=0.90        # Lower for faster generation
   HF_MAX_TOKENS=1500   # Reduce if possible
   ```

### Benchmark Results

| Configuration | VRAM | Speed | Quality |
|---------------|------|-------|---------|
| Full (bfloat16) | 60GB | 35 tok/s | Excellent |
| AWQ Quant | 16GB | 32 tok/s | Very Good |
| GPTQ Quant | 14GB | 30 tok/s | Good |
| Multi-GPU 2x | 30GB | 65 tok/s | Excellent |

---

## Troubleshooting

### Connection Errors

**Problem**: `Failed to connect to vLLM server at http://localhost:8000/v1`

**Solution**:
1. Check if vLLM is running: `ps aux | grep vllm`
2. Verify port 8000 is open: `netstat -tlnp | grep 8000`
3. Test connection: `curl http://localhost:8000/v1/models`

### Out of Memory (OOM)

**Problem**: `CUDA out of memory`

**Solution**:
1. Use quantization: `--quantization awq`
2. Reduce GPU memory utilization: `--gpu-memory-utilization 0.8`
3. Use smaller batch size
4. Close other GPU-using applications

### Model Download Fails

**Problem**: `Failed to download model from HuggingFace`

**Solution**:
1. Login to HF: `huggingface-cli login`
2. Check internet connection
3. Pre-download: `huggingface-cli download Jackrong/...`
4. Check disk space (need ~60GB)

### Slow Generation

**Problem**: Low tokens/second

**Solution**:
1. Check GPU utilization: `nvidia-smi`
2. Increase temperature: `HF_TEMPERATURE=0.9`
3. Reduce max tokens: `HF_MAX_TOKENS=1000`
4. Enable tensor parallelism: `--tensor-parallel-size 2`

### Wrong Reasoning Format

**Problem**: Model doesn't output thinking blocks

**Solution**:
1. Ensure thinking is enabled: `THINKING_ENABLED=true`
2. Use reasoning-optimized SLM: `get_hf_slm_with_reasoning()`
3. Check prompt includes reasoning instructions
4. Verify model loaded correctly

---

## Production Deployment

### Systemd Service

Create `/etc/systemd/system/vllm-naukri.service`:

```ini
[Unit]
Description=vLLM Server for NaukriAgent
After=network.target

[Service]
Type=simple
User=naukri
WorkingDirectory=/path/to/NaukriAgent
ExecStart=/usr/bin/python -m vllm.entrypoints.openai.api_server \
    --model Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled \
    --dtype bfloat16 \
    --gpu-memory-utilization 0.9 \
    --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable vllm-naukri
sudo systemctl start vllm-naukri
```

### Docker Deployment

```dockerfile
FROM nvidia/cuda:12.1-runtime-ubuntu22.04

RUN pip install vllm torch

WORKDIR /app

CMD ["python", "-m", "vllm.entrypoints.openai.api_server", \
     "--model", "Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled", \
     "--dtype", "bfloat16", \
     "--port", "8000"]
```

Build and run:

```bash
docker build -t vllm-naukri .
docker run --gpus all -p 8000:8000 vllm-naukri
```

---

## Model Information

**Model**: Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled

### Specifications

| Property | Value |
|----------|-------|
| Base Model | Qwen3.5-27B |
| Parameters | 27 Billion |
| Reasoning | Claude-4.6-Opus Distilled |
| Context Window | 262K tokens |
| Generation Speed | 29-35 tok/s |
| Memory (full) | ~60GB VRAM |
| Memory (AWQ) | ~16-20GB VRAM |
| License | Apache 2.0 |

### Capabilities

- ✓ Analytical reasoning with structured thinking
- ✓ Code generation and analysis
- ✓ Mathematical problem-solving
- ✓ Multi-turn conversations
- ✓ Tool calling / function execution
- ✓ Long context understanding (262K)
- ✓ Chain-of-thought reasoning

### Special Features

- **Thinking Mode**: Transparent reasoning with `<think>` tags
- **Efficient Reasoning**: Reduced redundant thinking loops
- **Developer Role Support**: Native support for coding agents
- **Extended Context**: 262K context window for long documents

---

## References

- [HuggingFace Model Page](https://huggingface.co/Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled)
- [vLLM Documentation](https://docs.vllm.ai/)
- [Qwen3.5 Documentation](https://qwenlm.github.io/)
- [LangChain vLLM Integration](https://python.langchain.com/docs/integrations/llms/vllm)

---

## Support & Issues

For issues:

1. Check [Troubleshooting](#troubleshooting) section
2. Review vLLM logs: `journalctl -u vllm-naukri -f`
3. Check HuggingFace model card
4. File issue on GitHub repository

---

**Last Updated**: March 28, 2026
**Status**: Production Ready
