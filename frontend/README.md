# StudyGemma

An AI-powered study buddy for CS students that transforms messy lecture notes into clear explanations, quizzes, practice problems, and interview prep material using Gemma 4.

![StudyGemma UI](https://your-image-url.png)

## 🎯 What It Does

StudyGemma takes your messy CS notes and transforms them into various study formats:

- **Explain**: Clear, beginner-friendly explanations with examples
- **Quiz Me**: 5-question quizzes to test your understanding
- **Notebook Notes**: Concise bullet-point summaries ready for studying
- **Practice Problems**: Generated practice problems to reinforce concepts
- **Interview Mode**: Technical interview prep based on your notes

Perfect for CS students who want to transform scattered notes into polished study material instantly.

## 🚀 Getting Started

### Prerequisites

- Node.js (v16+)
- Python 3.8+
- API keys for:
  - OpenRouter (free tier available)
  - Google AI Studio (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/studygemma.git
   cd studygemma
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows:
   .\venv\Scripts\Activate.ps1
   # On Mac/Linux:
   source venv/bin/activate
   
   pip install fastapi uvicorn python-dotenv requests
   ```

3. **Create `.env` file in `backend/` folder**
   ```
   OPENROUTER_API_KEY=your_openrouter_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   ```

### Running the Project

**Terminal 1 - Start the backend:**
```bash
cd backend
.\venv\Scripts\Activate.ps1  # (Windows) or source venv/bin/activate (Mac/Linux)
uvicorn main:app --reload
```
Backend runs on: `http://127.0.0.1:8000`

**Terminal 2 - Start the frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs on: `http://localhost:5173`

Open your browser to `http://localhost:5173` and start studying!

## 🏗️ Architecture

### Frontend
- **Framework**: React + Vite
- **Styling**: Custom CSS with dark mode support
- **Features**: Responsive design, smooth animations, mode selection

### Backend
- **Framework**: FastAPI (Python)
- **Models**: Gemma 4 via OpenRouter + Google AI API
- **Fallback**: Automatically tries OpenRouter first, falls back to Google AI if rate limited
- **CORS**: Enabled for local development

### Models Used
- **Primary**: `google/gemma-4-26b-a4b-it:free` (OpenRouter)
- **Fallback**: `gemma-4-26b-a4b-it` (Google AI Studio)
- **Context Length**: 262K tokens (perfect for long study sessions)

## 📋 Environment Variables

Create a `.env` file in the `backend/` folder:

```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxx
GOOGLE_API_KEY=AIzaSyxxxxx
```

**Where to get these keys:**
- OpenRouter: https://openrouter.ai/keys
- Google AI Studio: https://aistudio.google.com/app/apikey

## 📁 Project Structure

```
studygemma/
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── main.py
│   ├── .env (not tracked)
│   ├── venv/
│   └── requirements.txt
└── README.md
```

## 🎓 How to Use

1. **Paste your notes** into the textarea
2. **Choose a study mode** (Explain, Quiz Me, Notes, Practice, Interview)
3. **Click "Study with Gemma"**
4. **See your results** rendered beautifully below

Example use cases:
- Paste messy lecture notes → Get a structured explanation
- Paste code snippets → Get practice problems
- Paste textbook excerpts → Get interview prep questions

## 🔧 Troubleshooting

**Backend won't start?**
- Make sure venv is activated
- Check that FastAPI is installed: `pip install fastapi uvicorn`

**Frontend can't connect to backend?**
- Make sure backend is running on `http://127.0.0.1:8000`
- Check CORS is enabled (it is by default)

**Getting rate limit errors?**
- The backend automatically falls back to Google AI API
- Wait a few minutes if both APIs are rate limited
- Consider adding your own OpenRouter key for higher limits

**API keys not working?**
- Verify keys are in `.env` file (not quotes needed)
- Check that `.env` is in the `backend/` folder
- Restart the backend after adding/changing keys

## 🚀 Deployment

To deploy this project:

1. **Backend**: Deploy FastAPI to services like Heroku, Railway, or Replit
2. **Frontend**: Deploy React build to Vercel, Netlify, or GitHub Pages
3. Update frontend API endpoint from `http://127.0.0.1:8000` to your deployed backend

## 📝 License

MIT License - feel free to use this for learning and projects!

## 🙏 Credits

Built with:
- [Gemma 4](https://gemini.google.dev/) - The incredible open model
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [OpenRouter](https://openrouter.ai/) - Model access
- [Google AI Studio](https://aistudio.google.com/) - Free API access

## 📞 Questions?

Found a bug? Have a suggestion? Open an issue on GitHub!

---

**Built for the Gemma 4 Challenge** ✨