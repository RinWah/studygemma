# StudyGemma

An AI-powered study companion that transforms lecture notes into structured study materials using LLMs — built end-to-end with a React frontend and FastAPI backend.

## What it does

StudyGemma takes raw lecture notes and generates study-ready materials (summaries, key concepts, practice questions — *adjust to what it actually generates*) using Google's Gemma large language model. It's designed to help students turn unstructured notes into something they can actually study from, fast.

## Tech Stack

- **Frontend:** React
- **Backend:** FastAPI (Python)
- **LLM:** Gemma, accessed via OpenRouter and Google AI APIs
- **Reliability:** Intelligent API fallback logic — automatically switches between OpenRouter and Google AI when one is rate-limited, so the app stays responsive instead of failing on a single provider's limits

## Why I built it

*(1-2 sentences — e.g. "I built this after noticing how much time I spent reformatting my own lecture notes before exams, and wanted to see how far I could get automating that with an LLM pipeline.")*

## Key engineering decisions

- **Fallback routing between LLM providers** — rather than hard-coding a single API, the backend detects rate limiting and reroutes requests to a secondary provider, improving uptime without user-facing errors
- *(Add 1-2 more if relevant — e.g. how you handled prompt structuring, chunking long notes, caching, etc.)*

## Running it locally

```bash
# Clone the repo
git clone https://github.com/rinwah/studygemma.git
cd studygemma

# Backend setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend setup (in a new terminal)
cd frontend
npm install
npm run dev
```

*(Adjust folder names/commands to match your actual project structure)*

## Environment Variables

You'll need API keys for:
- `OPENROUTER_API_KEY`
- `GOOGLE_AI_API_KEY`

## Status

*(e.g. "Actively maintained" or "Completed as a personal project, May–July 2026")*

## License

*(MIT / none specified — your call)*