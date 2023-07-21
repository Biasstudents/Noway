import asyncio
import httpx
from concurrent.futures import ThreadPoolExecutor

url = input("Enter the website URL (including http or https): ")
num_threads = int(input("Enter the number of threads to use: "))
duration = int(input("Enter the duration of the stress test in seconds: "))

async def stress_test(client):
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            response = await client.get(url)
        except Exception as e:
            pass # Suppress error messages

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [asyncio.ensure_future(stress_test(client)) for _ in range(num_threads)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
