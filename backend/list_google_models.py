#!/usr/bin/env python3
"""
List all available models on Google AI API
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

print("=" * 70)
print("GOOGLE AI - AVAILABLE MODELS")
print("=" * 70)

if not GOOGLE_API_KEY:
    print("❌ No GOOGLE_API_KEY found in .env")
    exit(1)

print("✓ GOOGLE_API_KEY found\n")
print("Fetching available models...\n")

try:
    response = requests.get(
        url="https://generativelanguage.googleapis.com/v1beta/models",
        params={
            "key": GOOGLE_API_KEY
        },
        timeout=15
    )

    print(f"Status: {response.status_code}\n")
    data = response.json()
    
    if response.status_code == 200:
        if "models" in data:
            models = data["models"]
            print(f"Found {len(models)} available model(s):\n")
            
            for model in models:
                model_id = model.get("name", "").replace("models/", "")
                display_name = model.get("displayName", "")
                input_tokens = model.get("inputTokenLimit", 0)
                
                print(f"ID: {model_id}")
                print(f"Name: {display_name}")
                print(f"Max tokens: {input_tokens}")
                print()
        else:
            print("No models found in response")
            print(f"Response: {data}")
    else:
        print(f"Error: {data}")

except Exception as e:
    print(f"Failed: {str(e)}")
