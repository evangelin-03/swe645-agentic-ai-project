# SWE645 Extra Credit: Agentic AI System 

Submission By:

Evangelin Kopela – G01502543

Jenish Patel – G01551940

Aswin Rajendran – G01524875

Dhanush Neelakantan – G01503107

Lavanesh Mahendran – G01545858

## Overview

This project implements a fully functional Agentic AI System using LangGraph for workflow orchestration, Gemini 2.5 Pro for reasoning and planning, and FAISS for long-term memory storage. The system demonstrates modern Agentic AI principles including autonomous reasoning, tool calling, routing logic, memory integration, and multi-step planning with human-in-the-loop confirmation.

## Application URLs

### GitHub Repository

- **Source Code**: https://github.com/evangelin-03/swe645-agentic-ai-project

### Execution

- **Local Execution**: `python -m agent.main`
- **Environment Setup**: Add Gemini API key to `.env` file

## Architecture

### System Components

- **LLM**: Gemini 2.5 Pro for reasoning, planning, and question answering
- **Orchestration**: LangGraph state machine for workflow control
- **Tool Integration**: Custom calculator tool for safe math evaluation
- **Short-Term Memory**: Session state stores recent conversation context
- **Long-Term Memory**: FAISS vector database for persistent storage
- **Human-in-the-loop**: User confirmation required before plan execution


### High-Level Workflow

The system follows a multi-step pipeline:

1. User sends message to agent
2. Gemini creates execution plan
3. Plan is shown to user for approval (HITL)
4. If approved → system routes to tool or model
5. Output is generated and returned to user
6. Conversation is stored using FAISS memory
7. Memory can later be retrieved via `retrieve:` queries

## Files Structure

├── agent/
│   ├── main.py                 # Main CLI with HITL and memory updates
│   ├── langgraph_config.py     # LangGraph workflow (LLM → Router → Tool)
│   ├── tools/
│   │   └── calculator.py       # Math evaluation tool
│   └── memory/
│       ├── faiss_store.py      # FAISS database for long-term memory
│       └── seed_faiss.py       # Seeder for example vector entries
├── requirements.txt            # Python dependencies
├── README.md                   # This documentation
└── .gitignore                  # Ignores venv and secrets

## Deployment Instructions

### Prerequisites

1. Python 3.10 or higher
2. pip package manager
3. Gemini API key from Google AI Studio
4. Git installed

### Step 1: Clone Repository

git clone https://github.com/evangelin-03/swe645-agentic-ai-project.git
cd swe645-agentic-ai-project

### Step 2: Create Virtual Environment

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

### Step 3: Install Dependencies

pip install -r requirements.txt

### Step 4: Configure Environment Variables

Create a .envcd ~/swe645-agent
cat .gitignore
 file in the root directory:

```
GEMINI_API_KEY=YOUR_KEY_HERE
```

### Step 5: Run the Agent
python -m agent.main


## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: agent**
   - Solution: Run using `python -m agent.main` from project root

2. **FAISS errors**
   - Solution: Reinstall faiss-cpu using `pip install faiss-cpu`

3. **Gemini "model not found" error**
   - Solution: Use `models/gemini-2.5-pro` or `gemini-2.5-flash` in configuration

### Useful Commands

# Run the agent
python -m agent.main

# Check Python version
python --version

# List installed packages
pip list

# Install/update requirements
pip install -r requirements.txt

# Reinstall FAISS if errors occur
pip install --force-reinstall faiss-cpu

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Deactivate virtual environment
deactivate

# Test calculator tool
python -m agent.tools.calculator

# Seed FAISS memory with examples
python -m agent.memory.seed_faiss

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Check for missing dependencies
pip check

## Contributions

This project was completed collaboratively by 5 team members with equal distribution of work:

### Evangelin Kopela

- Implemented the LangGraph agent architecture (state machine, nodes, edges)
- Integrated Gemini 2.5 Pro for reasoning, planning, and multi-step execution
- Developed the FAISS long-term memory system, including embeddings and retrieval

### Jenish Patel

- Developing the tool-calling pipeline, including calculator tool integration
- Helped refine the human-in-the-loop flow for plan confirmation
- Contributed to documentation, clearly mapping features to assignment requirements

### Aswin Rajendran

- Built the agent's routing logic for deciding between LLM, tools, or ending execution
- Developed FAISS memory testing, validating correct retrieval behavior
- Developed parts of the CLI orchestrator and worked debug runtime flow

### Dhanush Neelakantan

- Worked on short-term memory behavior and session context handling
- Created presentation slides and demo walkthrough materials
- Assisted with GitHub repo organization and file structuring

### Lavanesh Mahendran

- Performed testing and validation of agent behavior and outputs
- Created the architecture diagram for system visualization
- Worked on report formatting, visuals, and clarity

## Assignment Requirements Fulfilled

### Required Components

| Requirement | Status |
|-------------|--------|
| LLM Reasoning & Planning | ✅ Completed |
| Tool Integration | ✅ Calculator tool |
| Short-term Memory | ✅ In session state |
| Long-term Memory (FAISS) | ✅ Implemented |
| Human-in-the-loop | ✅ Approval prompts |
| Agent Framework | ✅ LangGraph |
| Multi-step pipeline | ✅ Model → Router → Tool |
| Documentation | ✅ README + Diagram |
| Working Demo | ✅ CLI agent |
| GitHub Repo | ✅ Complete |

### Summary

✅ **LLM Reasoning & Planning**: Gemini 2.5 Pro provides autonomous reasoning
✅ **Tool Integration**: Calculator tool with safe evaluation
✅ **Short-term Memory**: In-session state management
✅ **Long-term Memory (FAISS)**: Vector database for persistent storage
✅ **Human-in-the-loop**: Approval prompts before execution
✅ **Agent Framework**: LangGraph orchestration
✅ **Multi-step Pipeline**: Model → Router → Tool workflow
✅ **Documentation**: Comprehensive README and architecture diagram
✅ **Working Demo**: Fully functional CLI agent
✅ **GitHub Repository**: Complete source code and documentation


