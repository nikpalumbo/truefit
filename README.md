# TrueFit

**TrueFit** is a LangGraph-based assistant that helps generate and review tailored cover letters using extracted user and company data.

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
```

> Make sure `.env` is in your `.gitignore` to avoid committing secrets.

### 5. Run with LangGraph Dev
```bash
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
