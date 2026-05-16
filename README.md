# AI Weather Assistant

An AI-powered weather assistant built using:

- LangChain
- Ollama
- Qwen3
- OpenWeatherMap API

The assistant can:

- Fetch real-time weather data
- Suggest clothing based on temperature
- Recommend activities based on weather conditions
- Stream AI responses in real-time

---

# Features

- Local AI model using Ollama
- LangChain agent architecture
- Weather API integration
- Tool calling support
- Streaming responses
- Clothing recommendations
- Activity suggestions

---

# Tech Stack

- Python
- LangChain
- Ollama
- Qwen3
- OpenWeatherMap API
- Requests
- UV package manager

---

# Installation

## Clone Repository

```bash
git clone <your_repo_url>
cd weatherLesson
```

---

## Install Dependencies

Using UV:

```bash
uv sync
```

---

## Install Ollama

Download Ollama:

https://ollama.com

---

## Pull Qwen Model

```bash
ollama pull qwen3:4b
```

---

## Create Environment Variables

Create a `.env` file:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

Get API key from:

https://openweathermap.org/api

---

# Run Ollama

```bash
ollama run qwen3:4b
```

---

# Run Project

```bash
uv run main.py
```

---

# Example Questions

- What is the weather in Lagos?
- What should I wear in London today?
- Is Tokyo good for outdoor activities?

---

# Project Structure

```text
weatherLesson/
│
├── main.py
├── README.md
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── .venv/
```

---

# Future Improvements

- Multi-city comparison
- Voice assistant support
- Weather forecasting
- Memory/chat history
- GUI frontend
- Autonomous travel planning

---

# Author

Built as a LangChain + Ollama learning project.