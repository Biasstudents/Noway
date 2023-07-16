import aiohttp
import asyncio

async def stress_test(url, num_requests, session):
    tasks = []
    for i in range(num_requests):
        if i % 2 == 0:
            tasks.append(session.get(url))
        else:
            tasks.append(session.head(url))
    await asyncio.gather(*tasks)

async def main(num_requests):
    url = input("Enter the website URL (including http or https): ")
    duration = int(input("Enter the duration of the stress test in seconds: "))
    connector = aiohttp.TCPConnector(limit=0)
    timeout = aiohttp.ClientTimeout(total=0)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < duration:
            print(f"Sending {num_requests} requests")
            await stress_test(url, num_requests, session)
            await asyncio.sleep(1)

if __name__ == '__main__':
    num_requests = 10000
    asyncio.run(main(num_requests))
