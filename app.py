from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from groq import Groq
import os

app = FastAPI()

# 1. CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. GROQ CLIENT - THIS LINE IS CRITICAL
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.get("/")
async def read_root():
    return FileResponse('index.html')

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    
    # Call Groq
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a SQL assistant. Convert user request to SQL query only."},
            {"role": "user", "content": user_message}
        ]
    )
    
    sql_query = completion.choices[0].message.content
    return {"response": sql_query}
