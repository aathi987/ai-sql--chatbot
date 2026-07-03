from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(question: Question):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that converts natural language to SQL queries. Only return the SQL query, no explanation."
            },
            {
                "role": "user",
                "content": question.question,
            }
        ],
        model="llama-3.1-70b-versatile",
    )
    answer = chat_completion.choices[0].message.content
    return {"answer": answer}

# THIS SERVES YOUR index.html FILE
@app.get("/")
async def read_index():
    return FileResponse('index.html')