from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import time

# ✅ Define FastAPI app instance
app = FastAPI()

# ✅ Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Allow all origins (adjust in production)
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # ✅ Allow all headers
)

# ✅ Define LLM API URL
LLM_API_URL = "http://llm-api:11434"

def call_llm_old(query, context):
    """Retries LLM API call in case of failure."""
    for attempt in range(5):  # Retry up to 5 times
        try:
            payload = {
                "model": "gemma:2b",  # ✅ Ensure correct model name
                "prompt": query,
                "stream": False
            }
            response = requests.post(f"{LLM_API_URL}/api/generate", json=payload)
            response_data = response.json()
            return response_data.get("response", "No response received.")
        except requests.exceptions.ConnectionError:
            print(f"⚠️ LLM API not ready, retrying... ({attempt+1}/5)")
            time.sleep(5)

    raise Exception("LLM API is unreachable after 5 retries.")

# ✅ Ensure this is correctly defined **AFTER** app is initialized
@app.post("/query")
async def query_rag(request: Request):
    data = await request.json()
    query_text = data["query"]

    # Call LLM API with retry logic
    response = call_llm(query_text, context={})
    return {"response": response}


def call_llm(query, context):
    """Retries LLM API call in case of failure."""
    for attempt in range(5):
        try:
            payload = {
                "model": "gemma:2b",  # Change this if you're using tinyllama or another model
                "messages": [
                    {"role": "system", "content": "You are a helpful coding assistant."},
                    {"role": "user", "content": query}
                ],
                "stream": False
            }
            response = requests.post(f"{LLM_API_URL}/api/chat", json=payload)
            response_data = response.json()

            # Handle responses - Ollama returns a 'message' key in response
            return response_data.get("message", {}).get("content", "No response received.")

        except requests.exceptions.ConnectionError:
            print(f"⚠️ LLM API not ready, retrying... ({attempt+1}/5)")
            time.sleep(5)

    raise Exception("LLM API is unreachable after 5 retries.")
