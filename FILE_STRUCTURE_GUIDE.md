# File Structure & Quick Reference

## Complete Project Structure

```
NaukriAgent/
│
├── 📋 Configuration Files
│   ├── config.py                  # Ollama-based SLM config
│   ├── config_hf.py              # HuggingFace vLLM config ⭐ NEW
│   ├── .env.example              # Environment template
│   └── requirements.txt           # Python dependencies (updated)
│
├── 📊 State Management
│   └── state.py                  # AgentState TypedDict (shared)
│
├── 🤖 OLLAMA-BASED WORKFLOW (Original)
│   ├── agents.py                 # Ollama agents & crew
│   ├── nodes.py                  # 6 workflow nodes
│   ├── workflow.py               # LangGraph builder
│   └── main.py                   # Entry point
│
├── 🤖 HUGGINGFACE-BASED WORKFLOW (New) ⭐
│   ├── agents_hf.py              # HF agents & crew
│   ├── nodes_hf.py               # HF workflow nodes
│   ├── workflow_hf.py            # HF LangGraph builder
│   └── main_hf.py                # HF entry point
│
├── 📚 Documentation
│   ├── README.md                 # General documentation
│   ├── QUICKSTART.md             # Quick start guide
│   ├── HF_SETUP_GUIDE.md         # HuggingFace setup ⭐ NEW
│   └── HF_INTEGRATION_SUMMARY.md # Integration overview ⭐ NEW
│
└── 📄 License & Meta
    └── LICENSE
```

---

## Quick Comparison

### File Mapping: Ollama → HuggingFace

| Ollama | HuggingFace | Purpose |
|--------|-------------|---------|
| config.py | config_hf.py | LLM initialization |
| agents.py | agents_hf.py | CrewAI agents |
| nodes.py | nodes_hf.py | Workflow nodes |
| workflow.py | workflow_hf.py | LangGraph workflow |
| main.py | main_hf.py | Entry point |
| (shared) | state.py | State definition |

---

## Getting Started

### Choose Your Path

#### 🟢 Path 1: Ollama (Easiest)
```bash
# 1. Install
pip install -r requirements.txt

# 2. Start Ollama
ollama serve

# 3. Run
python main.py
```
**Best for**: Quick testing, laptop usage

#### 🔵 Path 2: HuggingFace vLLM (Recommended)
```bash
# 1. Install
pip install -r requirements.txt

# 2. Start vLLM
python -m vllm.entrypoints.openai.api_server \
    --model Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled \
    --port 8000

# 3. Run
python main_hf.py
```
**Best for**: Production, better reasoning, reasoning chains visible

---

## Model Comparison

| Feature | Ollama | HuggingFace vLLM |
|---------|--------|------------------|
| Model | Varies (phi3, llama2, etc.) | Qwen3.5-27B-Claude-Opus |
| Reasoning | Basic | Advanced (Claude distilled) |
| Reasoning Chains | Hidden | Visible `<think>` blocks |
| Parameters | Various | 27 Billion |
| Memory | Varies | 60GB / 16GB (quantized) |
| Speed | Medium | Fast (35 tok/s) |
| Context Window | Limited | Large (262K tokens) |
| Setup Complexity | Very Easy | Moderate |
| Best For | Development | Production |

---

## Configuration Reference

### Ollama Setup (.env)
```env
SLM_MODEL_NAME=phi-3-fine-tuned-hr
SLM_BASE_URL=http://localhost:11434/v1
SLM_API_KEY=ollama
```

### HuggingFace Setup (.env)
```env
HF_MODEL_ID=Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled
VLLM_BASE_URL=http://localhost:8000/v1
HF_DTYPE=bfloat16
THINKING_ENABLED=true
```

---

## Workflow Architecture (Both Paths)

### Identical 6-Node Structure

```
START
  ↓
[Node 1: Validate Inputs]
  ↓
[Nodes 2-3: CrewAI Analysis]
  ├─ Agent: Resume Analyzer
  ├─ Agent: JD Matcher
  └─ Agent: Skill Assessor (optional)
  ↓
[Node 4: Scoring Engine]
  ├─ Skill Match (60%)
  ├─ Experience Match (40%)
  └─ Reasoning Adjustments
  ↓
[Node 5: Human Approval]
  ├─ Approve → [Node 6: Finalize]
  └─ Reject → END
  ↓
[Node 6: Finalize & Shortlist]
  ↓
END
```

---

## Key Functions

### config.py vs config_hf.py

```python
# Ollama
from config import get_slm()

# HuggingFace
from config_hf import get_hf_slm()
from config_hf import get_hf_slm_with_reasoning()  # With <think> blocks
```

### agents.py vs agents_hf.py

```python
# Ollama
from agents import run_analysis_crew(resume, jd, slm)

# HuggingFace
from agents_hf import run_analysis_crew_hf(resume, jd, slm, use_reasoning=True)
from agents_hf import compare_analysis_approaches(resume, jd)
```

### nodes.py vs nodes_hf.py

```python
# Ollama nodes
validate_inputs(), run_crew_analysis(), scoring_engine()
human_approval(), generate_shortlist()

# HuggingFace nodes (same pattern)
validate_inputs_hf(), run_crew_analysis_hf(), scoring_engine_hf()
human_approval_hf(), generate_shortlist_hf()

# Reasoning analysis (HF only)
analyze_reasoning_chain(state)
```

### workflow.py vs workflow_hf.py

```python
# Ollama
from workflow import get_compiled_app()

# HuggingFace
from workflow_hf import get_compiled_app_hf()
```

### main.py vs main_hf.py

```python
# Ollama
from main import run_workflow()

# HuggingFace
from main_hf import run_workflow_hf()
from main_hf import compare_workflows()  # Compare both
```

---

## Usage Examples

### Example 1: Run Ollama Workflow

```python
from main import run_custom_workflow

result = run_custom_workflow(
    resume="Senior Python Engineer with 5+ years...",
    jd="Looking for Senior Backend Developer...",
    candidate_name="John Doe",
    candidate_email="john@example.com"
)

print(f"Status: {result['status']}")
print(f"Score: {result['overall_score']}%")
```

### Example 2: Run HuggingFace Workflow

```python
from main_hf import run_custom_workflow_hf

result = run_custom_workflow_hf(
    resume="Senior Python Engineer...",
    jd="Senior Backend Developer...",
    candidate_name="Jane Smith",
    candidate_email="jane@example.com"
)

print(f"Status: {result['status']}")
print(f"Score: {result['overall_score']}%")
```

### Example 3: Compare Both Approaches

```python
from main_hf import compare_workflows

# Runs same candidate through both systems
compare_workflows()
```

### Example 4: Analyze Reasoning Chain

```python
from workflow_hf import get_compiled_app_hf
from nodes_hf import analyze_reasoning_chain

app = get_compiled_app_hf()
final_state = app.stream(inputs)

reasoning_info = analyze_reasoning_chain(final_state)
print(f"Thinking blocks: {len(reasoning_info['thinking_blocks'])}")
print(f"Has reasoning: {reasoning_info['reasoning_present']}")
```

---

## Environment Setup

### Required Files

1. **requirements.txt** ✅ - Contains all dependencies
2. **.env** - Create from .env.example

### Choose Python Environment

```bash
# Option 1: Virtual Environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option 2: Conda
conda create -n naukri python=3.10
conda activate naukri
pip install -r requirements.txt

# Option 3: Docker
docker build -t naukri .
docker run -it naukri
```

### GPU Setup

```bash
# For NVIDIA GPUs
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Check GPU availability
python -c "import torch; print(torch.cuda.is_available())"
```

---

## Troubleshooting Checklist

### For Ollama

- [ ] Ollama installed: `ollama version`
- [ ] Server running: `curl http://localhost:11434/v1/models`
- [ ] Model available: `ollama list`
- [ ] .env configured correctly
- [ ] Import errors fixed: `pip install -r requirements.txt`

### For HuggingFace vLLM

- [ ] vLLM installed: `python -m vllm --version`
- [ ] Server running: `curl http://localhost:8000/v1/models`
- [ ] GPU available: `nvidia-smi`
- [ ] .env configured correctly
- [ ] Model downloaded: `huggingface-cli download Jackrong/...`

---

## Documentation Index

| Document | Purpose | Best For |
|----------|---------|----------|
| README.md | General overview | Getting started |
| QUICKSTART.md | 5-min setup | New users |
| HF_SETUP_GUIDE.md | Detailed HF setup | HF deployment |
| HF_INTEGRATION_SUMMARY.md | Feature comparison | Choosing approach |
| This file | Quick reference | Looking up info |

---

## Command Reference

### Ollama Commands

```bash
# Start server
ollama serve

# List models
ollama list

# Pull model
ollama pull phi3

# Run model
ollama run phi3

# Check specific model
ollama show phi3:latest
```

### vLLM Commands

```bash
# Start server
python -m vllm.entrypoints.openai.api_server --model <model_id> --port 8000

# Download model
huggingface-cli download <model_id>

# Check GPU
nvidia-smi

# Kill server
pkill -f vllm
```

### NaukriAgent Commands

```bash
# Run Ollama workflow
python main.py

# Run HuggingFace workflow
python main_hf.py

# Show HF model info
python config_hf.py

# Show HF workflow info
python workflow_hf.py
```

---

## Performance Benchmarks

### Ollama (phi3)
- Memory: ~8GB
- Speed: 15-25 tok/s
- Reasoning: Basic
- Setup: Very easy

### HuggingFace vLLM (Qwen3.5-Claude-Opus)
- Memory: 60GB full / 16GB quantized
- Speed: 29-35 tok/s
- Reasoning: Advanced (Claude distilled)
- Setup: Moderate

---

## Next Steps

1. **Choose your path**: Ollama or HuggingFace?
2. **Follow setup guide**: README.md or HF_SETUP_GUIDE.md
3. **Configure .env**: Copy from .env.example
4. **Start your backend**: Ollama or vLLM
5. **Run workflow**: main.py or main_hf.py
6. **Evaluate results**: Check scores and analysis

---

**Date**: March 28, 2026
**Version**: 1.0 (Complete)
**Status**: Production Ready
