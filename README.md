# 🤖 Ilgın Tandoğan - AI Assistant (Digital Twin)

Welcome to my interactive resume! I built this AI-powered application to demonstrate my ability to develop and deploy working products using modern technologies.

Instead of reading a static PDF, you can chat with this AI to learn about my **DevOps experience, certifications, and technical skills.**

🔗 **Live Demo:** [Click here to chat with my AI](BURAYA_STREAMLIT_LINKINI_YAPISTIRACAKSIN)

## 🚀 How It Works
This project uses **RAG (Retrieval-Augmented Generation)** principles:
1.  **Data Source:** My professional background is structured in a JSON format (`data.json`).
2.  **LLM:** It utilizes **Google's Gemini 1.5 Flash** model to understand natural language queries.
3.  **Context Injection:** When you ask a question, the system feeds my resume data into the model as context to generate accurate, personalized responses.

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Interface:** Streamlit (for rapid frontend development)
* **AI Model:** Google Gemini API (Generative AI)
* **Deployment:** Streamlit Community Cloud

## 📂 Project Structure
```text
├── app.py           # Main application logic
├── data.json        # Structured resume data (The Knowledge Base)
├── requirements.txt # Project dependencies
└── README.md        # Documentation
