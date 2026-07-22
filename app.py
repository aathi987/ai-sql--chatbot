from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
import psycopg2
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

# Initialize Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# PostgreSQL Connection (YOUR CODE - UNCHANGED)
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

# Request Model
class ChatRequest(BaseModel):
    message: str

# Home Route
@app.get("/")
async def home():
    return FileResponse("index.html")

# Chat Route
@app.post("/chat")
async def chat(request: ChatRequest):

    prompt = f"""
You are an AI SQL Assistant.

Convert the following English question into a valid PostgreSQL SQL query.

Only return the SQL query.
Do not include explanations.
Do not include markdown.

Question:
{request.message}
"""

    try:
        # Generate SQL
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

        sql = response.choices[0].message.content.strip()

        # Remove markdown if present
        sql = sql.replace("```sql", "").replace("```", "").strip()

        # Connect to PostgreSQL
        conn = get_connection()
        cur = conn.cursor()

        # Execute SQL
        cur.execute(sql)

        # If SELECT query
        if sql.lower().startswith("select"):
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]

            result = []
            for row in rows:
                result.append(dict(zip(columns, row)))
        else:
            conn.commit()
            result = [{"message": "Query executed successfully"}]

        cur.close()
        conn.close()

        return {
            "sql": sql,
            "result": result
        }

    except Exception as e:
        return {
            "sql": "",
            "error": str(e)
        }
      
