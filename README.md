# 🧠 WhatsApp Legal Assistant Bot (FastAPI)

This is a FastAPI-based backend for a WhatsApp chatbot that answers legal questions using AI.

### 🔧 Features
- Retrieves legal context using a local database
- Generates responses using OpenRouter AI models
- Sends structured answers back to WhatsApp
- Designed for Indian legal use cases

### 🚀 Endpoints
- `POST /` — Receives messages from WhatsApp and returns AI-generated legal advice

### 🛠️ Tech Stack
- Python
- FastAPI
- OpenRouter (Mistral-7B-Instruct)
- WhatsApp Cloud API

---

### 👇 Deployment Instructions (for HF team)
Make sure `.env` contains the following:
- `OPENROUTER_API_KEY`
- `OPENROUTER_MODEL`
- `REFERER_URL`
- `WHATSAPP_TOKEN`
- `VERIFY_TOKEN`

This Space is Docker-free and runs with `requirements.txt`.
