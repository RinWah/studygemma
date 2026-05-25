from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StudyRequest(BaseModel):
    notes: str
    mode: str

SYSTEM_PROMPT = """
You are StudyGemma, an AI tutor for computer science students.

Your goals:
- explain concepts clearly
- generate concise notebook notes
- create quizzes
- generate practice problems
- teach in a beginner-friendly way

Always:
- use clean formatting
- avoid unnecessary jargon
- use examples when helpful
- be concise but useful
"""

# Global variables to store selected provider and model
selected_provider = None
selected_model = None

def get_available_gemma_model():
    """
    Fetches available Gemma models from OpenRouter and selects the best free option.
    Returns the model identifier string.
    """
    global selected_model
    
    # If we've already selected a model, use it
    if selected_model:
        return selected_model
    
    try:
        print("Fetching available Gemma models from OpenRouter...")
        
        # Get list of available models
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            }
        )
        
        if response.status_code != 200:
            print(f"Failed to fetch models: {response.status_code}")
            return None
        
        models_data = response.json()
        
        # Extract Gemma models that support free pricing
        gemma_models = []
        
        if "data" in models_data:
            for model in models_data["data"]:
                model_id = model.get("id", "")
                
                # Check if it's a Gemma model
                if "gemma" in model_id.lower():
                    # Check if it has free pricing
                    pricing = model.get("pricing", {})
                    prompt_price = float(pricing.get("prompt", "1"))
                    completion_price = float(pricing.get("completion", "1"))
                    
                    # Free models have 0 cost
                    if prompt_price == 0 and completion_price == 0:
                        gemma_models.append({
                            "id": model_id,
                            "name": model.get("name", ""),
                            "context_length": model.get("context_length", 0)
                        })
        
        # Sort by context length (larger is better for studying)
        gemma_models.sort(key=lambda x: x["context_length"], reverse=True)
        
        if gemma_models:
            selected_model = gemma_models[0]["id"]
            print(f"✓ Selected OpenRouter model: {selected_model}")
            print(f"  Name: {gemma_models[0]['name']}")
            print(f"  Context length: {gemma_models[0]['context_length']}")
            return selected_model
        else:
            print("No free Gemma models found on OpenRouter")
            return None
    
    except Exception as e:
        print(f"Error fetching models from OpenRouter: {str(e)}")
        return None

def call_openrouter(model, prompt):
    """
    Call OpenRouter API with the given model and prompt.
    Returns the response text or None if it fails.
    """
    try:
        print(f"Attempting OpenRouter with model: {model}")
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=30
        )

        data = response.json()
        print(f"OpenRouter response status: {response.status_code}")
        print(f"OpenRouter response: {data}")

        # Check for rate limiting or other errors
        if response.status_code != 200:
            print(f"OpenRouter failed with status {response.status_code}")
            return None

        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            print(f"OpenRouter error: {data}")
            return None

    except Exception as e:
        print(f"OpenRouter error: {str(e)}")
        return None

def call_google_api(prompt):
    """
    Call Google AI API directly with Gemma model.
    Returns the response text or None if it fails.
    """
    if not GOOGLE_API_KEY:
        print("No GOOGLE_API_KEY in .env file")
        return None
    
    try:
        print("Attempting Google AI API (fallback)")
        
        response = requests.post(
            url="https://generativelanguage.googleapis.com/v1beta/models/gemma-4-26b-a4b-it:generateContent",
            headers={
                "Content-Type": "application/json",
            },
            params={
                "key": GOOGLE_API_KEY
            },
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            },
            timeout=30
        )

        data = response.json()
        print(f"Google API response status: {response.status_code}")
        print(f"Google API response: {data}")

        if response.status_code != 200:
            print(f"Google API failed with status {response.status_code}")
            return None

        if "candidates" in data and len(data["candidates"]) > 0:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"Google API error: {data}")
            return None

    except Exception as e:
        print(f"Google API error: {str(e)}")
        return None

@app.get("/")
def home():
    return {"message": "StudyGemma backend is running"}

@app.get("/health")
def health():
    """Health check endpoint that also initializes the model."""
    global selected_model
    if not selected_model:
        model = get_available_gemma_model()
        return {
            "status": "healthy",
            "model": model,
            "has_google_key": bool(GOOGLE_API_KEY)
        }
    return {
        "status": "healthy",
        "model": selected_model,
        "has_google_key": bool(GOOGLE_API_KEY)
    }

@app.post("/study")
def study(request: StudyRequest):

    try:
        mode_instructions = {
            "explain": "Explain the notes simply with examples.",
            "quiz me": "Create 5 quiz questions based on the notes.",
            "notebook notes": "Create concise notebook-ready bullet point notes.",
            "practice problems": "Generate practice problems based on the notes.",
            "interview mode": "Teach this like technical interview prep."
        }

        instruction = mode_instructions.get(
            request.mode.lower(),
            "Explain clearly."
        )

        prompt = f"""
{SYSTEM_PROMPT}

TASK:
{instruction}

STUDENT NOTES:
{request.notes}
"""

        # Try OpenRouter first
        model = get_available_gemma_model()
        if model:
            output = call_openrouter(model, prompt)
            if output:
                return {"response": output}
            else:
                print("OpenRouter failed, trying Google API...")
        else:
            print("No OpenRouter model available, trying Google API...")

        # Fallback to Google API
        output = call_google_api(prompt)
        if output:
            return {"response": output}
        else:
            return {
                "response": "Backend error: Both OpenRouter and Google API failed. Check your API keys and rate limits."
            }

    except Exception as e:
        print("ERROR:")
        print(str(e))

        return {
            "response": f"Backend error: {str(e)}"
        }