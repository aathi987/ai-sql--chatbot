from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from groq import Groq
from dotenv import load_dotenv
import psycopg2
import os


load_dotenv()


app = FastAPI()

<<<<<<< HEAD

=======
# 1. CORS FIX
>>>>>>> 246d1535c2153ff6d17d71fedf94c3682ddacc1e
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
=======
# 2. GROQ CLIENT - THIS LINE IS CRITICAL
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
>>>>>>> 246d1535c2153ff6d17d71fedf94c3682ddacc1e

@app.get("/")
async def read_root():
    return FileResponse('index.html')



@app.post("/chat")
async def chat(request: Request):
<<<<<<< HEAD

    data = await request.json()
    user_message = data.get("message")

    try:
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a PostgreSQL expert.

Convert the user's request into PostgreSQL SQL.

Return ONLY SQL.
No explanation.
No markdown.
No ```sql.
"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0
        )

        sql_query = completion.choices[0].message.content.strip()

        sql_query = (
            sql_query
            .replace("```sql", "")
            .replace("```", "")
            .strip()
        )

        
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = conn.cursor()

        
        cur.execute(sql_query)

        
        if sql_query.lower().startswith("select"):
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]

            result = []

            for row in rows:
                result.append(dict(zip(columns, row)))

            cur.close()
            conn.close()

            return {
                "sql": sql_query,
                "result": result
            }

        
        else:
            conn.commit()

            cur.close()
            conn.close()

            return {
                "sql": sql_query,
                "result": "Query executed successfully."
            }

    except Exception as e:
        return {
            "error": str(e)
        }
=======
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
>>>>>>> 246d1535c2153ff6d17d71fedf94c3682ddacc1e

    
    
