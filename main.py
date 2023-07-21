import asyncio
import httpx
from colorama import Fore, Style, init

init()

print("Layer 7: get, head")
protocol = input("Enter the method to use: ")

if protocol in ["get", "head"]:
    url = input("Enter the website URL (including http or https): ")
else:
    print(Fore.RED + f"Invalid protocol: {protocol}" + Style.RESET_ALL)
    exit(1)

num_threads = int(input("Enter the number of threads to use: "))
duration = int(input("Enter the duration of the stress test in seconds: "))

packet_counter = 0

async def stress_test(client):
    global packet_counter
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            if protocol == "get":
                response = await client.get(url)
            elif protocol == "head":
                response = await client.head(url)
            packet_counter += 1
        except Exception as e:
            pass # Suppress error messages

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [stress_test(client) for _ in range(num_threads)]
        await asyncio.gather(*tasks)

print(Fore.YELLOW + f"Stress testing started on {url} successfully!" + Style.RESET_ALL)
asyncio.run(main())
print(Fore.YELLOW + f"Stress test ended. Sent {packet_counter} requests in total." + Style.RESET_ALL)
