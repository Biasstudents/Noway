import aiohttp
import asyncio
import threading

# Set the number of threads to use
num_threads = 1000

# Set the URL of the website to test
url = "https://tls.mrrage.xyz/nginx_status"

# Create a TCPConnector with an unlimited connection pool
connector = aiohttp.TCPConnector(limit=0)

async def stress_test():
    async with aiohttp.ClientSession(connector=connector) as session:
        while True:
            await send_request(session)

async def send_request(session):
    async with session.get(url) as response:
        print(f"Status code: {response.status}")

def run_stress_test():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(stress_test())

# Create and start the threads
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=run_stress_test)
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()
