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
    connector = aiohttp.TCPConnector(limit=0)
    timeout = aiohttp.ClientTimeout(total=0)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        while True:
            try:
                response = await session.get(url)
                response.raise_for_status()
                print(f"Website is up, sending {num_requests} requests")
                await stress_test(url, num_requests, session)
            except (aiohttp.ClientError, aiohttp.ClientResponseError):
                print(f"Website is down, sending {num_requests // 2} requests")
                await stress_test(url, num_requests // 2, session)
            await asyncio.sleep(1)

if __name__ == '__main__':
    num_requests = 1000
    asyncio.run(main(num_requests))
