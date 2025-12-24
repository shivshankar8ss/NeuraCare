# 🧠NeuraCare – Intelligent Support for Mental Wellness

NeuraCare is an AI-powered mental health companion designed to demonstrate how **tool-using AI agents** can support empathetic conversations while safely integrating real-world actions.

The project combines a **FastAPI backend**, a **LangGraph-based AI agent**, and a **Streamlit chat UI**, with optional **WhatsApp integration via Twilio**. It is built as a practical demo of modern AI system design rather than a medical product.

## 🌟 What NeuraCare Does

NeuraCare acts as a conversational AI assistant that can:

- Hold **empathetic, supportive conversations** about mental well-being
- Decide when to use **external tools** based on user intent
- Trigger **emergency actions** in high-risk scenarios
- Provide **location-aware therapist suggestions**
- Work across **web (Streamlit)** and **WhatsApp (Twilio)**

The focus of this project is **responsible AI agent orchestration**, not diagnosis or treatment.

---

## ✨ Key Features

### 💬 Empathetic AI Conversations
- Powered by a MedGemma-based LLM (via Groq)
- Responds with warmth, normalization, and gentle guidance
- Keeps conversations open-ended and supportive

### 🧠 Tool-Using AI Agent
- Built using **LangGraph (ReAct-style agent)**
- The agent reasons about:
  - When to answer directly
  - When to call a tool
  - Which tool is appropriate

### 🚨 Emergency Call Tool
- If the agent detects crisis signals (self-harm intent, suicidal ideation):
  - Triggers a **Twilio voice call** to a predefined emergency/helpline number
- Demonstrates **safety-aware AI behavior**

### 📍 Therapist Finder Tool
- Finds nearby therapists based on a user-provided location
- Supports:
  - Google Maps API (Places + Geocoding)
  - OpenStreetMap (via Geopy) as a free alternative
- Designed to **fail gracefully** if location services are unavailable

### 🌐 Web Chat UI
- Simple, clean **Streamlit chat interface**
- Maintains conversation state
- Displays which tool (if any) was used

### 📲 WhatsApp Integration
- Uses **Twilio WhatsApp webhooks**
- Accepts form-encoded messages
- Responds using **TwiML**
- Ideal for demonstrating multi-channel AI systems

---

## 🏗️ Project Architecture

```text
NeuraCare/
├── backend/
│   ├── ai_agent.py      # LangGraph agent + tool definitions
│   ├── main.py          # FastAPI app (REST + Twilio webhook)
│   ├── tools.py         # LLM, Twilio, and helper integrations
│   ├── config.py        # API keys & configuration (not committed)
│   └── test_location_tool.py  # Location tool testing
│
├── frontend.py          # Streamlit web chat UI
├── pyproject.toml       # Dependencies & environment config
└── README.md
