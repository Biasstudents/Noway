import aiohttp
import asyncio

async def stress_test(url, num_requests):
    connector = aiohttp.TCPConnector(limit=0)
    timeout = aiohttp.ClientTimeout(total=0)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        for i in range(num_requests):
            if i % 2 == 0:
                tasks.append(session.get(url))
            else:
                tasks.append(session.head(url))
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    url = 'https://www.example.com'
    num_requests = 10000
    asyncio.run(stress_test(url, num_requests))
