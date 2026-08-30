# 🤖 AI Research Assistant

A multi-agent AI research assistant that searches the web, analyzes information using a local Large Language Model (LLM), validates findings, and generates structured research reports.

The project is designed to demonstrate practical AI engineering concepts including agent orchestration, web research, LLM integration, backend APIs, and modern frontend development.

---

## 🚀 Project Overview

The AI Research Assistant accepts a research question from the user and performs the following workflow:

User Query
    ↓
React Frontend
    ↓
FastAPI Backend
    ↓
Research Orchestrator
    ↓
Tavily Web Search
    ↓
Source Processing
    ↓
Analysis Agent
    ↓
Ollama + Llama 3.2 1B
    ↓
Critic / Validation Agent
    ↓
Report Generation
    ↓
Final Research Report

The goal is to build a reliable research system that provides answers based on retrieved sources instead of relying only on the LLM's internal knowledge.

---

## ✨ Planned Features

- 🔎 Web research using Tavily
- 🤖 Local LLM using Ollama
- 🧠 Multi-agent architecture
- 📚 Source-based research
- 🔗 Source URLs and citations
- 📝 Automatic research report generation
- 🔍 Evidence-based analysis
- ⚖️ Contradiction detection
- ✅ Research validation
- 🌐 React web interface
- ⚡ FastAPI backend
- 🔐 Environment-based API key management
- 🧪 Automated testing
- 📊 Research progress/status tracking

---

## 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │      User        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ React Frontend   │
                    │     + Vite       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ FastAPI Backend  │
                    └────────┬─────────┘
                             │
                             ▼
                 ┌────────────────────────┐
                 │ Research Orchestrator │
                 └───────────┬────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
     ┌────────────────┐            ┌────────────────┐
     │ Tavily Search  │            │  LLM Service   │
     │                │            │                │
     │ Web Sources    │            │ Ollama         │
     └───────┬────────┘            │ Llama 3.2 1B   │
             │                     └───────┬────────┘
             │                             │
             └──────────────┬──────────────┘
                            ▼
                    ┌─────────────────┐
                    │ Analysis Agent  │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │ Critic Agent    │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │ Report Agent    │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │ Final Report    │
                    └─────────────────┘
