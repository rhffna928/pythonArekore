from fastapi import FastAPI
from time import time
import httpx
import asyncio

app = FastAPI()

URL = "http://httpbin.org/uuid"

async def request(client):
    response = await client.get(URL)
    return response.text

async def task():
    async with httpx.AsyncClient() as client:
        tasks = [request(client) for i in range(100)]
        result = await asyncio.gather(*tasks)
        print(result)

@app.get('/')
async def f():
    start = time()
    await task()
    print("time:",time() - start)