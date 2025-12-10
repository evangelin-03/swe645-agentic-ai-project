# SWE645 Extra Credit: Agentic AI System (LangGraph + Gemini + FAISS)

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
- **Short-Term Memory**: Session state stores recent conversation context (last 5 messages)
- **Long-Term Memory**: FAISS vector database with sentence-transformers for persistent storage
- **Human-in-the-loop**: User confirmation required before plan execution

### Major Components

| Component | Description | Implementation |
|-----------|-------------|----------------|
| Gemini LLM | Generates plans, answers questions, routes decisions | `google-genai` library |
| LangGraph State Machine | Controls execution flow between model, tools, and memory | `SimpleGraph` class in `langgraph_config.py` |
| Calculator Tool | Safe evaluation of math expressions | `calculator.py` with regex validation |
| Short-Term Memory | Stores last 5 user messages during session | In-memory list in `main.py` |
| FAISS Long-Term Memory | Stores embeddings of past interactions | `FaissMemory` class with `all-MiniLM-L6-v2` embeddings |
| Human-in-the-loop | Confirms plan execution before running | CLI confirmation prompt in `main.py` |

### High-Level Workflow

The system follows a multi-step pipeline:

1. **User Input**: User sends message to agent via CLI
2. **Context Building**: Short-term memory (last 5 messages) is prepended to the prompt
3. **Plan Generation**: Gemini LLM creates execution plan with system instruction
4. **Tool Detection**: Agent detects if calculator tool is needed via regex pattern matching
5. **Human Approval**: Plan is shown to user for approval (HITL)
6. **Execution**: If approved, system routes to tool or executes LLM response
7. **Memory Storage**: Conversation is stored in FAISS with embeddings
8. **Retrieval**: Memory can be queried via `retrieve: <query>` commands

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         User Input                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Short-Term Memory (Session)                    │
│              (Last 5 Messages Context)                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  LangGraph Orchestrator                     │
│                    (SimpleGraph Class)                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Gemini 2.5 Pro LLM                        │
│              (Plan Generation & Reasoning)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Router / Tool Detection                    │
│              (Regex Pattern Matching)                       │
└──────────┬────────────────────────────┬─────────────────────┘
           │                            │
    Calculator Tool              Standard LLM Response
           │                            │
           ▼                            ▼
┌──────────────────┐         ┌─────────────────────┐
│  safe_eval_math  │         │  Gemini Execution   │
│   (eval tool)    │         │    (text response)  │
└──────────┬───────┘         └──────────┬──────────┘
           │                            │
           └────────────┬───────────────┘
                        │
                        ▼
           ┌────────────────────────┐
           │  Human-in-the-Loop     │
           │  (Approval Required)   │
           └────────────┬───────────┘
                        │
                        ▼
           ┌────────────────────────┐
           │   Execute & Return     │
           │      Result            │
           └────────────┬───────────┘
                        │
                        ▼
           ┌────────────────────────┐
           │  FAISS Long-Term       │
           │  Memory Storage        │
           │  (Embeddings + Meta)   │
           └────────────────────────┘
```

## Files Structure

```
├── agent/
│   ├── __init__.py             # Package marker
│   ├── main.py                 # Main CLI with HITL and memory updates
│   ├── langgraph_config.py     # LangGraph workflow (LLM → Router → Tool)
│   ├── tools/
│   │   ├── __init__.py         # Package marker
│   │   └── calculator.py       # Math evaluation tool
│   └── memory/
│       ├── __init__.py         # Package marker
│       ├── faiss_store.py      # FAISS database for long-term memory
│       ├── seed_faiss.py       # Seeder for example vector entries
│       └── faiss_data/
│           ├── index.faiss     # FAISS vector index (generated)
│           └── meta.json       # Document metadata (generated)
├── requirements.txt            # Python dependencies
├── hello_gemini.py            # Simple Gemini API test script
├── README.md                   # This documentation
└── .gitignore                  # Ignores venv and secrets
```

## Deployment Instructions

### Prerequisites

1. **Python 3.10 or higher**
2. **pip package manager**
3. **Gemini API key** from [Google AI Studio](https://aistudio.google.com/app/apikey)
4. **Git** installed

### Step 1: Clone Repository

```bash
git clone https://github.com/evangelin-03/swe645-agentic-ai-project.git
cd swe645-agentic-ai-project
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `python-dotenv>=1.0.0` - Environment variable management
- `google-genai>=0.3.0` - Gemini API client
- `langgraph>=0.2.0` - Agent orchestration framework
- `langchain-core>=0.3.0` - Core LangChain utilities
- `faiss-cpu>=1.7.4` - Vector database for memory
- `sentence-transformers` - Text embeddings (auto-installed with faiss)

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

**To get your Gemini API key:**
1. Visit https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key and paste it in your `.env` file

### Step 5: (Optional) Seed FAISS Memory

```bash
python -m agent.memory.seed_faiss
```

This adds example documents to the FAISS vector database for testing retrieval.

### Step 6: Run the Agent

```bash
python -m agent.main
```


## Usage Examples

### Example 1: Math Tool Usage (Tool Use Path)

```
User> 1+4

=== AGENT PLAN ===
CALCULATE: 1+4

Execute plan? (y/n) > y
Result: 5
Saved to memory with id 8cb1ff8fc9b4
```

### Example 2: Complex Math Expression

```
User> calculate: (25 * 3) + 17 / 2

=== AGENT PLAN ===
Calculator executed: (25 * 3) + 17 / 2

Execute plan? (y/n) > y
Result: 83.5
Saved to memory with id a4f2d9e1c7b8
```

### Example 3: Normal LLM Question

```
User> What is LangGraph?

=== AGENT PLAN ===
LangGraph is a library for building stateful, multi-actor applications 
with Large Language Models (LLMs). It extends LangChain by representing 
workflows as graphs with nodes (actors) and edges (transitions), enabling 
cyclical flows essential for agent-like behaviors such as re-planning, 
retrying failed tools, and looping until conditions are met.

Execute plan? (y/n) > y
Result: [Detailed explanation provided by Gemini]
Saved to memory with id 3d8a7b9f2e1c
```

### Example 4: Long-Term Memory Retrieval

```
User> retrieve: math calculations

--- Memory Results ---
- ID: 8cb1ff8fc9b4  Score: 0.8452
  Text: User: 1+4
Agent: 5

- ID: a4f2d9e1c7b8  Score: 0.7891
  Text: User: calculate: (25 * 3) + 17 / 2
Agent: 83.5
```

### Example 5: Human-in-the-Loop Rejection

```
User> What's the weather?

=== AGENT PLAN ===
I don't have access to real-time weather data. I would need a weather 
API tool to check current conditions.

Execute plan? (y/n) > n
Execution aborted by human.
```

## Monitoring and Features

### Core Capabilities

✅ **Autonomous LLM Reasoning**: Gemini 2.5 Pro generates plans and answers  
✅ **Dynamic Tool Calling**: Regex-based routing to calculator tool  
✅ **Human-in-the-Loop**: Approval system for every action  
✅ **Short-Term Memory**: Session context with last 5 messages  
✅ **FAISS Vector Database**: Persistent long-term memory with embeddings  
✅ **Intelligent Routing**: Conditional logic for tool vs. LLM responses  
✅ **Modular Architecture**: Clean separation of concerns across modules  

### System Specifications

| Component | Technology | Details |
|-----------|-----------|---------|
| **LLM** | Gemini 2.5 Pro | `models/gemini-2.5-pro` |
| **Embedding Model** | all-MiniLM-L6-v2 | 384-dimensional vectors |
| **Vector DB** | FAISS | IndexFlatL2 (L2 distance) |
| **Framework** | LangGraph | Custom SimpleGraph implementation |
| **Tool Protocol** | Regex Pattern | CALCULATE: or direct expression |
| **Memory Limit** | 5 messages | Short-term conversation window |

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: agent**
   - **Cause**: Running script from wrong directory
   - **Solution**: Always run from project root using `python -m agent.main`

2. **FAISS errors: "dimension mismatch"**
   - **Cause**: Embedding model changed or corrupted index
   - **Solution**: Delete `agent/memory/faiss_data/` folder and re-run to rebuild index
   ```bash
   rm -rf agent/memory/faiss_data/
   python -m agent.memory.seed_faiss
   ```

3. **Gemini "model not found" error**
   - **Cause**: Invalid model name
   - **Solution**: Use `models/gemini-2.5-pro` or `models/gemini-2.5-flash` in configuration

4. **ImportError: No module named 'google.genai'**
   - **Cause**: Missing dependencies
   - **Solution**: Reinstall requirements
   ```bash
   pip install -r requirements.txt
   ```

5. **API Key Error: "GEMINI_API_KEY not set"**
   - **Cause**: Missing or incorrect `.env` file
   - **Solution**: Create `.env` file with valid API key
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```

### Useful Commands

```bash
# Run the agent
python -m agent.main

# Test Gemini API connection
python hello_gemini.py

# Check Python version (requires 3.10+)
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

# Seed FAISS memory with examples
python -m agent.memory.seed_faiss

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Check for missing dependencies
pip check

# View FAISS index info
python -c "from agent.memory.faiss_store import FaissMemory; m=FaissMemory(); print(f'Documents: {m.index.ntotal}')"
```



## Contributions

This project was completed collaboratively by 5 team members with equal distribution of work:

### Evangelin Kopela

- Implemented the full LangGraph agent architecture (state machine, nodes, edges)
- Integrated Gemini 2.5 Pro for reasoning, planning, and multi-step execution
- Developed the FAISS long-term memory system, including embeddings and retrieval

### Aswin Rajendran

- Built the agent's routing logic for deciding between LLM, tools, or ending execution
- Developed FAISS memory testing, validating correct retrieval behavior
- Developed parts of the CLI orchestrator and helped debug runtime flow

### Jenish Patel

- Developed the tool-calling pipeline, including calculator tool integration
- Helped refine the human-in-the-loop flow for plan confirmation
- Contributed to documentation, clearly mapping features to assignment requirements

### Dhanush Neelakantan

- Worked on short-term memory behavior and session context handling
- Created presentation slides and demo walkthrough materials
- Assisted with GitHub repo organization and file structuring

### Lavanesh Mahendran

- Performed testing and validation of agent behavior and outputs
- Created the architecture diagram for system visualization
- Worked on report formatting, visuals, and clarity


