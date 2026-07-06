from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Groq API Key
client = Groq(api_key="YOUR_GROQ_API_KEY")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def home():
    return FileResponse("index.html")

@app.post("/chat")
async def chat(request: ChatRequest):

    prompt = f"""
You are an AI SQL Assistant.

Convert the following English question into SQL.

Only return the SQL query.

Question:
{request.message}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        sql = response.choices[0].message.content

        return {
            "response": sql
        }

    except Exception as e:
        return {
            "response": str(e)
        }