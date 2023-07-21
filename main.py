import aiohttp
import asyncio
import time
import argparse
from colorama import Fore, Style, init

init()

parser = argparse.ArgumentParser(description="Stress testing tool.")
parser.add_argument("-method", choices=["get", "head", "tcp", "udp"], help="Choose the method to use.")
args = parser.parse_args()

method = args.method

if not method:
    method = input("Choose the method to use (get, head, tcp, udp): ")

url = None
ip = None
port = None
if method in ["get", "head"]:
    url = input("Enter the website URL (including http or https): ")
elif method in ["tcp", "udp"]:
    ip = input("Enter the IP address of the server: ")
    port = int(input("Enter the port number: "))

num_threads = int(input("Enter the number of threads to use: "))
duration = int(input("Enter the duration of the stress test in seconds: "))

packet_size = 65507 if method == "udp" else 65535

packet_counter = 0

async def stress_test(thread_id, packet_counter_lock):
    global packet_counter

    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        last_print_time = start_time - 9
        if thread_id == 0:
            if method in ["get", "head"]:
                print(Fore.YELLOW + f"Stress testing started on {url}" + Style.RESET_ALL)
            elif method in ["tcp", "udp"]:
                print(Fore.YELLOW + f"Stress testing started on {ip}:{port}" + Style.RESET_ALL)

        while time.time() - start_time < duration:
            if method in ["get", "head", "tcp", "udp"]:
                await send_packet(session)
                async with packet_counter_lock:
                    packet_counter += 1
            if thread_id == 0 and time.time() - last_print_time >= 10:
                async with packet_counter_lock:
                    if method in ["get", "head"]:
                        try:
                            response_start_time = time.time()
                            response = await session.get(url) if method == "get" else await session.head(url)
                            response_end_time = time.time()
                            response_time = round((response_end_time - response_start_time) * 1000, 2)
                            print(Fore.GREEN + f"Website is up. Response time: {response_time} ms." + Style.RESET_ALL)
                        except Exception as e:
                            print(Fore.RED + f"Website is down." + Style.RESET_ALL)
                    elif method in ["tcp", "udp"]:
                        print(f"Sent {packet_counter} packets to {ip}:{port}")
                    last_print_time = time.time()

async def send_packet(session):
    try:
        if method == "tcp":
            response = await session.get(f"http://{ip}:{port}")
        elif method == "udp":
            response = await session.get(f"udp://{ip}:{port}")
    except Exception as e:
        pass

async def main():
    # Create the packet_counter_lock object inside the main function
    packet_counter_lock = asyncio.Lock()

    tasks = []
    for i in range(num_threads):
        task = asyncio.create_task(stress_test(i, packet_counter_lock))
        tasks.append(task)

    await asyncio.gather(*tasks)

    print(Fore.YELLOW + "Stress test ended." + Style.RESET_ALL)

asyncio.run(main())
