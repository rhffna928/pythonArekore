import sqlite3
from fastapi import FastAPI

app = FastAPI()
DB_FILE = "/data/mqtt_messages.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            payload TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.post("/save")
async def save_message(topic: str, payload: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (topic, payload) VALUES (?, ?)", (topic, payload))
    conn.commit()
    conn.close()
    return {"status": "Message saved"}

init_db()
