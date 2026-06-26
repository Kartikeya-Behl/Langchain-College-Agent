# 🎓 AI College Assistant Agent

An intelligent **AI-powered College Assistant** built with **LangChain**, **Ollama**, and **Qwen2.5**. The assistant uses a **tool-calling agent architecture** to interpret natural language queries, dynamically invoke specialized tools, and generate accurate responses for common university-related tasks.

Unlike a traditional chatbot with hardcoded logic, the agent autonomously decides which tool(s) to use based on the user's request, enabling multi-step reasoning and handling of complex queries.

## ✨ Features

- 🤖 Autonomous tool selection using LangChain Agents
- 📊 Attendance & Exam Eligibility Calculator
- 📝 Result, Grade & Pass/Fail Evaluation
- 💰 Fee Balance Calculator
- 📚 Library Fine Calculator
- 🏠 Hostel Fee Calculator
- 👨‍🎓 Student Information Retrieval
- 🔗 Multi-tool reasoning for compound queries
- 💬 Natural language interaction

---

## 🛠 Tech Stack

- Python
- LangChain
- LangChain Ollama
- Ollama
- Qwen2.5:3B
- Tool Calling Agents

---

## 🚀 Installation

```bash
git clone https://github.com/yourusername/langchain-college-agent.git
cd langchain-college-agent

pip install -r requirements.txt

ollama pull qwen2.5:3b

python main.py
```

---

## 💡 Example Queries

```text
I attended 72 classes out of 90.

My marks are 95, 90, 88, 91 and 87.

Show student details for Student ID S101.

I attended 80 classes out of 100, my marks are 90, 85, 88, 92 and 95, and I paid 45000 out of a 60000 fee. Give me my attendance, grade, and pending fee.
```

---

## ⚙️ How It Works

1. The user submits a natural language query.
2. The LangChain agent interprets the request.
3. The LLM identifies the required tool(s).
4. Selected tools are executed.
5. The agent synthesizes the tool outputs into a single response.

---

## 🔮 Future Improvements

- Persistent student database
- GPA/CGPA calculator
- RAG-based academic document search
- Timetable & faculty lookup
- Memory-enabled conversations
- Web interface
