# 🤖 IT Support Ticket Resolution Agent

An intelligent IT support ticket resolution system built with LangGraph and LangChain that automatically processes and resolves IT support tickets through AI-powered analysis and response generation.

## 📌 Project Overview

The agent processes IT support tickets through the following workflow:

1. **Classify** – Identifies ticket category (System, Network, Settings, General)
2. **Retrieve** – Fetches solutions from vector-embedded knowledge base
3. **Draft** – Generates professional response
4. **Review** – Evaluates response quality
5. **Retry/Escalate** – Handles complex cases

### 🔧 Technologies Used

- **LangGraph** – Orchestration and state flow  
- **Hugging Face** – `mistralai/Mistral-7B-Instruct-v0.2` for LLM  
- **Gradio** – User-friendly interface for ticket submission  
- **Clean Modular Architecture**

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)
- Hugging Face API token
- 8GB+ RAM for embeddings

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/meetrafay/IT-Support-Agent.git
cd IT-Support-Agent
```

2. **Set Up Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### Configure Environment

Create `.env` file:
```env
HUGGINGFACE_API_TOKEN=<your-token>
EMBED_MODEL="sentence-transformers/all-MiniLM-L6-v2"
```

### Set Up Knowledge Base

1. **Create Knowledge Base Directory**
```bash
mkdir -p src/agent/knowledge/json
```

This creates JSON files for each category with pre-defined solutions.

## 🚀 Usage

### Web Interface

1. **Start Gradio Server**
```bash
python -m src.agent.app
```

2. Open browser: [http://localhost:7860](http://localhost:7860)

3. **Submit Ticket:**
   - Subject (max 100 chars)
   - Description (max 500 chars)

### ✅ Start LangGraph UI (Optional)

```bash
langgraph dev
```

Then open: [http://localhost:8123](http://localhost:8123)

---

### API Usage

```python
from agent.graph import graph

ticket = {
    "subject": "System freezing",
    "description": "Computer freezes randomly during use"
}

result = graph.invoke({
    "ticket": ticket,
    "messages": [],
    "attempt": 0,
    "drafts": [],
    "feedbacks": []
})
```

## 📁 Project Structure

```
├── src/
│   └── agent/
│       ├── knowledge/         # Knowledge base files
│       │   ├── json/         # Category-wise solutions
│       │   └── indexes/      # FAISS indexes
│       ├── nodes/            # Graph node implementations
│       ├── app.py            # Gradio web interface
│       ├── graph.py          # LangGraph workflow
│       ├── prompts.py        # LLM prompts
│       ├── state.py          # State management
│       └── utils.py          # Helper functions
├── tests/
├── requirements.txt
└── .env
```

## 🧠 Knowledge Base Categories

### System
- Hardware issues
- Operating system problems
- Performance optimization
- Driver conflicts
- System crashes

### Network
- Connectivity issues
- Wi-Fi problems
- VPN access
- Network security
- Bandwidth issues

### Settings
- Application configuration
- User preferences
- System settings
- Security policies
- Access permissions

### General
- Software installation
- Account access
- File management
- Printer setup
- Email configuration

## 📈 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## 🧠 Design and Architectural Decisions

### ✅ Workflow Design

* **LangGraph**: Stateful orchestration for clear transitions & retry logic
* **Nodes**: Single-purpose modules:

  * `classify`
  * `retrieve`
  * `draft`
  * `review`
  * `retry_draft`
* **State**: Defined in `state.py` with fields:

  * `ticket`, `category`, `context`, `draft`, `approved`, `attempt`, `drafts`, `feedbacks`, `output`

---

### ✅ Modular Architecture

* **Nodes**: `src/agent/nodes/*.py`
* **Shared Logic**: `utils.py` (e.g., `call_llm`)
* **Knowledge Base**: Text files in `src/agent/knowledge/`

---

### ✅ Prompt Engineering

* `prompts.py`: Node-specific prompts

  * `classify_prompt`: Ensures only valid categories
  * `review_prompt`: Approves minor issues, reduces false escalations

---

### ✅ Error Handling

* **API Errors**: Graceful fallback in `utils.py`
* **Classify**: Defaults to `General` if LLM output invalid
* **Review**: Escalates if not clearly "Approved"
* **Retrieve**: Warns if file missing
* **Gradio**: Validates inputs:

  * Subject ≤100 chars
  * Description ≤500 chars

---

### ✅ Token Optimization

* `classify`: `max_tokens=50`
* `review`: `max_tokens=100`
* `draft`/`retry_draft`: `max_tokens=400`

---

### ✅ Traceability

* `state["messages"]`: Logs every step
* `escalation_log.csv`: Records all escalations
* **LangGraph UI**: Visual step-by-step
* **Gradio UI**: Shows processing state & result

---

### ✅ Gradio UI

Implemented in `app.py`:

* ✅ Loading indicator
* ✅ Input validation
* ✅ Displays:

  * Category
  * Draft
  * Feedback (if escalated)
* Runs on: [http://localhost:7860](http://localhost:7860)


### ✔️ Edge Cases

| Case                | Behavior                |
| ------------------- | ----------------------- |
| 🔄 Missing file     | Fallback message shown  |
| ❌ Invalid category  | Fallback to `General`   |
| 🔒 Bad API token    | Logs error + fallback   |
| 🖼️ Gradio UI fails | Check port 7860 is free |

---

## 📈 Future Improvements

* Add full docstrings and inline comments
* Dynamic loading of knowledge base
* Retry logic for API rate limits
* UI enhancements: history, visual trace

---

## 🧩 Troubleshooting

| Problem                      | Solution                                        |
| ---------------------------- | ----------------------------------------------- |
| **API Errors**               | Check `HUGGINGFACE_API_TOKEN` in `.env`         |
| **LangGraph UI not loading** | Ensure `langgraph.json` points to correct graph |
| **Gradio UI not loading**    | Free port `7860`, ensure `gradio` is installed  |
| **Drafts cut short**         | Increase `max_tokens=400` in `draft.py`         |
| **Unexpected escalations**   | Tweak `review_prompt`                           |
| **Input validation**         | Keep subject ≤100, description ≤500 chars       |

```