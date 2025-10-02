# TrueFit

**TrueFit** is an intelligent, LangGraph-based assistant designed to generate and review personalized cover letters by leveraging structured memory and Retrieval-Augmented Generation (RAG).

**Business Case:** https://sdw.solutions/case-studies/ai-agent-truefit
**Demo:** https://youtu.be/7kv31ifuI_8


Unlike standard LLMs, TrueFit combines multiple capabilities:

- 🧠 **Long-term memory**: It stores and recalls user information such as values, interests, and resumes using TrustCall.
- 🏢 **Company extraction**: It analyzes company data, extracting mission, values, and job details.
- 🔎 **Tavily-powered RAG**: When values or mission are missing, it uses Tavily search to enrich context by pulling fresh web content.
- ✍️ **Tailored generation**: Merges profile + company context to craft or evaluate cover letters.
- 🔄 **Feedback loop**: It can revise and score a letter against the job description.
- 🧾 **Dual LLM usage**: While GPT-4o powers extraction and generation, the review process uses Claude Sonnet for scoring and actionable feedback.
- 🛠️ **Built with LangGraph + LangSmith**: The entire application is designed as a composable LangGraph, enabling traceable logic, live debugging, and rapid iteration. LangSmith integration offers observability and monitoring during development.

This level of contextual personalization goes beyond typical LLM prompting. TrueFit acts as a dynamic agent with both memory and search to give you the best cover letter possible.

---

## 🚀 Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/nikpalumbo/truefit.git
cd truefit
```

### 2. Create Python Virtual Environment 
It has been tested with python3.13
```bash
python -m venv langchain-env
source langchain-env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```
Edit `.env` and set your API keys:
```env
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
TAVILY_API_KEY=your-tavily-key
LANGSMITH_API_KEY=your-langsmith-api-key
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_PROJECT="truefit"
```

> Make sure `.env` is in your `.gitignore` to avoid committing secrets.

### 5. Run with LangGraph Dev
```bash
pip install "langgraph-cli[inmem]"
langgraph dev
```
This will launch the graph in interactive development mode.

---

## 📁 Folder Structure
```
truefit/
├── nodes/               # LangGraph nodes for profile, company, review, etc.
├── models/              # Pydantic models and memory schemas
├── utils/               # Helper functions, extractors, spy, etc.
├── configuration.py     # User config schema for LangGraph
├── graph_builder.py     # StateGraph setup and compilation
├── .env.example         # Template for environment variables
├── requirements.txt     # Python dependencies
├── README.md            # Project setup and documentation
```

---

## ✅ Linting and Style
This project follows [Pylint](https://pylint.pycqa.org/) conventions.

To lint:
```bash
pylint .
```

To auto-format (optional):
```bash
pip install black
black .
```

---

## 🤝 Contributions
Feel free to fork the project and submit a pull request.

---
