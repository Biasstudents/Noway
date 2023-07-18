import aiohttp
import asyncio

# Set the number of tasks to use
num_tasks = 1000

# Set the URL of the website to test
url = "https://tls.mrrage.xyz/nginx_status"

async def stress_test():
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session) for _ in range(num_tasks)]
        await asyncio.gather(*tasks)

async def send_request(session):
    while True:
        async with session.get(url) as response:
            print(f"Status code: {response.status}")

# Run the stress test
asyncio.run(stress_test())
