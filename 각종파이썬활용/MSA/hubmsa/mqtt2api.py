from fastapi import FastAPI
import requests

app = FastAPI()

@app.post("/forward")
async def forward_message(message: dict):
    destination = message.get("destination", "http://external-service/api")
    response = requests.post(destination, json=message)
    return {"status": response.status_code, "message": "Forwarded successfully"}
