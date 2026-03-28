# NaukriAgent - AI-Powered Candidate Screening System

## Overview

**NaukriAgent** is an intelligent recruitment automation system that combines **LangGraph** for workflow orchestration and **CrewAI** for specialized agentic analysis. It streamlines the candidate screening process by automatically analyzing resumes against job descriptions using a fine-tuned Small Language Model (SLM).

### Key Features

- ✅ **Automated Resume Analysis** - Extract skills, experience, and qualifications
- ✅ **JD Matching** - Compare candidate profile against job requirements
- ✅ **Intelligent Scoring** - Calculate skill and experience alignment scores
- ✅ **Human-in-the-Loop** - Recruiter review and approval gate
- ✅ **Workflow State Management** - LangGraph-based reliable state tracking
- ✅ **Multi-Agent Collaboration** - CrewAI agents for specialized analysis
- ✅ **Extensible Architecture** - Easy to customize and extend

---

## Architecture

```
INPUT (Resume/JD)
        ↓
    [Node 1: Validate Inputs]
        ↓
    [Nodes 2-3: CrewAI Analysis]
        ├─→ Resume Analyzer Agent
        └─→ JD Matcher Agent
        ↓
    [Node 4: Scoring Engine]
        ↓
    [Node 5: Human Approval]
        ↓
    [Branch] Approved? 
        ├─→ YES → [Node 6: Finalize/Shortlist] → END
        └─→ NO → END (Rejection)
```

---

## Installation & Setup

### 1. Prerequisites

- **Python 3.10+**
- **pip** package manager
- **Ollama** or **vLLM** running locally with a fine-tuned model

### 2. Install Dependencies

```bash
cd /path/to/NaukriAgent
pip install -r requirements.txt
```

### 3. Configure Your SLM

Create a `.env` file:

```env
# SLM Configuration
SLM_MODEL_NAME=phi-3-fine-tuned-hr
SLM_BASE_URL=http://localhost:11434/v1
SLM_API_KEY=ollama

# Application Configuration
APPROVAL_REQUIRED=true
DEFAULT_SCORE_THRESHOLD=75
```

#### Running Ollama

```bash
# macOS
brew install ollama

# Start server
ollama serve

# In another terminal, run model
ollama pull phi3  # Or your fine-tuned model
```

#### Using vLLM

```bash
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/your/model \
    --port 8000
```

---

## Project Structure

```
NaukriAgent/
├── requirements.txt          # Dependencies
├── .env                      # Configuration (create this)
├── main.py                   # Entry point
├── config.py                 # SLM configuration
├── state.py                  # AgentState definition
├── agents.py                 # CrewAI agents
├── nodes.py                  # Workflow nodes
├── workflow.py               # LangGraph builder
└── README.md                 # Documentation
```

### File Descriptions

| File | Purpose |
|------|---------|
| **config.py** | Initialize SLM and load environment variables |
| **state.py** | Define `AgentState` TypedDict for workflow state |
| **agents.py** | Create CrewAI agents and crew setup |
| **nodes.py** | Implement 6 workflow node functions |
| **workflow.py** | Build LangGraph state machine |
| **main.py** | Entry point with execution logic |

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with SLM configuration
cp .env.example .env  # Or create manually

# 3. Start Ollama/vLLM server
ollama serve

# 4. Run the application
python main.py
```

---

## Usage

### Running with Sample Data

```bash
python main.py
```

The script will:
1. Load sample resume and job description
2. Execute workflow nodes sequentially
3. Prompt you to approve/reject the candidate
4. Output final results

### Custom Usage in Python

```python
from main import run_custom_workflow

resume = """Your candidate resume here"""
jd = """Your job description here"""

result = run_custom_workflow(
    resume=resume,
    jd=jd,
    candidate_name="John Doe",
    candidate_email="john@example.com"
)

print(f"Status: {result['status']}")
print(f"Score: {result['overall_score']}%")
```

### Using Workflow Directly

```python
from workflow import get_compiled_app

app = get_compiled_app()

inputs = {
    "resume": "...",
    "jd": "...",
    "analysis_results": "",
    "skill_match_score": 0.0,
    "experience_match_score": 0.0,
    "overall_score": 0,
    "status": "pending",
    "rejection_reason": "",
    "recruiter_notes": "",
    "candidate_name": "Candidate",
    "candidate_email": "candidate@example.com"
}

for output in app.stream(inputs):
    node_name = list(output.keys())[0]
    print(f"Executing: {node_name}")
```

---

## Workflow Nodes

### Node 1: Validate Inputs
- Validates resume and JD are provided
- Raises error if validation fails
- Confirms candidate information

### Nodes 2-3: CrewAI Analysis
- **Resume Analyzer**: Extracts skills, experience, certifications
- **JD Matcher**: Compares profile against requirements
- Uses fine-tuned SLM for both agents
- Returns detailed analysis with scores

### Node 4: Scoring Engine
- Calculates weighted scores:
  - Skill Match: 60%
  - Experience Match: 40%
- Generates overall score (0-100)

### Node 5: Human Approval
- Displays candidate summary and analysis
- Recruiter options: Approve/Reject/Request Info
- Captures recruiter notes and decision

### Node 6: Finalize & Shortlist
- Updates final candidate status
- Prepares notifications
- Generates shortlist records

---

## Configuration

### Environment Variables

```env
SLM_MODEL_NAME              # Your fine-tuned model name
SLM_BASE_URL                # Ollama/vLLM endpoint
SLM_API_KEY                 # API key for SLM
APPROVAL_REQUIRED           # Enable human approval
DEFAULT_SCORE_THRESHOLD     # Minimum score to advance
```

### Customizing Scores

Edit `nodes.py` `scoring_engine()` function:

```python
overall_score = int(
    (skill_score * 0.6) +        # Adjust weights
    (experience_score * 0.4)
)
```

---

## Advanced Features

### Conditional Routing

The workflow uses conditional edges to route based on approval:

```python
def route_decision(state):
    if state.get("status") == "approved":
        return "finalize"
    else:
        return "end"
```

### State Persistence

For production, integrate database:

```python
app = workflow.compile(
    checkpointer=PgCheckpointer(conn_string="postgresql://..."),
    interrupt_before=["approval"]
)
```

### Extending Agents

Add new agents in `agents.py`:

```python
def get_technical_screener(slm):
    return Agent(
        role='Technical Screener',
        goal='Assess technical depth',
        llm=slm
    )
```

---

## Troubleshooting

### Connection Error to SLM

**Problem**: `Failed to connect to SLM at http://localhost:11434/v1`

**Solution**:
1. Ensure Ollama/vLLM is running
2. Verify `.env` configuration
3. Test: `curl http://localhost:11434/v1/models`

### Import Errors

**Problem**: `Import "crewai" could not be resolved`

**Solution**:
```bash
pip install --upgrade crewai langchain-openai langgraph
```

### Score Extraction Issues

**Problem**: Scores show as defaults

**Solution**: Update regex patterns in `nodes.py` to match your SLM's output format.

---

## Performance Optimization

### Production Recommendations

1. **Enable Caching** - Store analysis results for identical inputs
2. **Async Processing** - Convert to async for parallel candidate evaluation
3. **Batch Processing** - Process multiple candidates efficiently
4. **Database Caching** - Persist analysis results

### Example: Async Workflow

```python
import asyncio

async def validate_inputs_async(state):
    # async implementation
    pass
```

---

## Contributing

Contributions welcome! To contribute:

1. Fork repository
2. Create feature branch (`git checkout -b feature/name`)
3. Make changes
4. Commit (`git commit -am 'Add feature'`)
5. Push (`git push origin feature/name`)
6. Open Pull Request

---

## License

MIT License - See LICENSE file

---

## Roadmap

- [ ] Web UI for recruiter review
- [ ] Database integration for state persistence
- [ ] Multi-language resume support
- [ ] PDF resume parsing
- [ ] Email notifications
- [ ] Analytics dashboard
- [ ] Candidate ranking board
- [ ] Job board integrations

---

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
3. Check [CrewAI Docs](https://docs.crewai.com/)

---

## Acknowledgments

- **LangGraph** - Workflow orchestration
- **CrewAI** - Multi-agent framework
- **LangChain** - LLM integration
- **Ollama** - Local LLM serving

---

**Last Updated**: March 28, 2026
**Status**: Production Ready
