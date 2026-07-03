from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import sqlite3
import os
import re
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
conn = sqlite3.connect("database.db", check_same_thread=False)
cur = conn.cursor()

def clean_sql(text):
    text = re.sub(r'sql|', '', text)
    text = text.replace(';', '').strip()
    return text

def is_safe_sql(sql):
    dangerous = ['drop', 'delete', 'update', 'insert', 'alter', 'truncate', 'create', 'replace']
    sql_lower = sql.lower()
    for word in dangerous:
        if word in sql_lower:
            return False
    return True

@app.post("/ask")
async def ask_db(request: Request):
    data = await request.json()
    query = data.get("query")

    schema = "Table: employees(id, name, department, salary). Department values are: Engineering, Marketing, HR. Use exact case."
    prompt = f"You are a SQL expert. Given schema: {schema}. Convert this to SQL: {query}. Only return SQL, no explanation, no markdown."

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}
        ],
        temperature=0
    )

    sql = clean_sql(response.choices[0].message.content)

    if not is_safe_sql(sql):
        return {"error": "Sorry, I can only read data. I cannot modify or delete.", "sql": sql}

    try:
        cur.execute(sql)
        result = cur.fetchall()

        if not result:
            answer = "No results found"
        elif len(result) == 1 and len(result[0]) == 1:
            answer = str(result[0][0])
        else:
            answer = "\n".join([", ".join(map(str, row)) for row in result])

        return {"answer": answer, "sql": sql}
    except Exception as e:
        return {"error": str(e), "sql": sql}