import asyncio
import aiohttp

def one():
    print("One")

async def fetch():
    url = 'https://python.org'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"Fetched {url} with status {response.status}")
            text = await response.text()
            print(text)

def two():
    print("Two")

async def main():
    one()
    await fetch()
    two()
