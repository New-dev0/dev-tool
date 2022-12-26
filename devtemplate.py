TEMPLATE = {
    "fastapi": """from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()

@app.get("/")
async def init():
    return "Hello World"

""",
    "telethon": """from telethon import TelegramClient

client =  TelegramClient("bot", api_id=6, api_hash="")
client.start()
""",
"aiohttp": """
import asyncio
url = ""

async def main():
    async with aiohttp.ClientSession() as ses:
        async with ses.get(url) as res:
            response = await res.read()

asyncio.run(main())
"""
}
