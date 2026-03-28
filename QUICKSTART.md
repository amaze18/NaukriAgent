# Quick Start Guide - NaukriAgent

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd /path/to/NaukriAgent
pip install -r requirements.txt
```

### Step 2: Configure SLM
```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your SLM details
# SLM_BASE_URL: http://localhost:11434/v1  (Ollama)
# SLM_MODEL_NAME: phi-3-fine-tuned-hr (or your model)
```

### Step 3: Start SLM Server

**Option A: Using Ollama**
```bash
# Install Ollama (if needed)
brew install ollama

# Start server in one terminal
ollama serve

# Pull model in another terminal
ollama pull phi3
```

**Option B: Using vLLM**
```bash
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/your/fine-tuned-model \
    --port 8000
```

### Step 4: Run NaukriAgent
```bash
python main.py
```

Follow the prompts to approve/reject the candidate!

---

## Project Files Overview

```
main.py          → Entry point, execute here
├── workflow.py   → LangGraph workflow builder
├── nodes.py      → Individual workflow nodes (6 nodes)
├── agents.py     → CrewAI agents setup
├── state.py      → AgentState TypedDict
└── config.py     → SLM configuration

requirements.txt → Install dependencies
.env            → Your configuration (create this)
.env.example    → Template configuration
README.md       → Full documentation
```

---

## What Each Node Does

| Node | Purpose | Input | Output |
|------|---------|-------|--------|
| 1 | Validate inputs | Resume, JD | Validated state |
| 2-3 | CrewAI analysis | Resume, JD | Analysis results + scores |
| 4 | Score calculation | Analysis | Overall score (0-100) |
| 5 | Human decision | Summary | Approval status |
| 6 | Finalize | Status | Final candidate record |

---

## Example: Running with Custom Data

Create a Python script:

```python
from main import run_custom_workflow

my_resume = """
John Doe
Senior Python Engineer with 6 years experience
Skills: Python, FastAPI, AWS, Docker, Kubernetes
"""

my_jd = """
Senior Backend Engineer
Requirements: 5+ years Python, Cloud experience
"""

result = run_custom_workflow(
    resume=my_resume,
    jd=my_jd,
    candidate_name="John Doe",
    candidate_email="john@example.com"
)

if result['status'] == 'approved':
    print("✓ Candidate approved!")
else:
    print("✗ Candidate rejected")
```

---

## Troubleshooting

### Can't connect to SLM
- Check Ollama/vLLM is running: `ps aux | grep ollama`
- Verify `.env` configuration
- Test connection: `curl http://localhost:11434/v1/models`

### ModuleNotFoundError
```bash
pip install --upgrade -r requirements.txt
```

### CrewAI agents not responding
- Ensure SLM server is running
- Check model is loaded: `ollama ls`
- Try pulling model again: `ollama pull phi3`

---

## Next Steps

1. ✅ Customize scoring weights in `nodes.py`
2. ✅ Add more agents in `agents.py`
3. ✅ Integrate with database for persistence
4. ✅ Build web UI for recruiter interface
5. ✅ Deploy to production environment

---

## Documentation

- Full docs: See [README.md](README.md)
- LangGraph: https://langchain-ai.github.io/langgraph/
- CrewAI: https://docs.crewai.com/
- Ollama: https://ollama.ai/

---

Need help? Check README.md or troubleshooting section!
