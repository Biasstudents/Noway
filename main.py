import cloudscraper
import httpx
import socket
import threading
import time
from colorama import Fore, Style, init

# Initialize colorama
init()

# Set the protocol/method to use for sending requests
protocol = input("Enter the protocol/method to use (tcp, udp, get, head, or cfb): ")

if protocol in ["get", "head", "cfb"]:
    # Set the URL of the website to test
    url = input("Enter the website URL (including http or https): ")
elif protocol in ["tcp", "udp"]:
    # Set the IP address and port of the server to test
    ip = input("Enter the IP address of the server: ")
    port = int(input("Enter the port number: "))

# Set the number of threads to use
num_threads = int(input("Enter the number of threads to use: "))

# Set the duration of the stress test in seconds
duration = int(input("Enter the duration of the stress test in seconds: "))

def stress_test(thread_id):
    if protocol == "cfb":
        client = cloudscraper.create_scraper()
    elif protocol in ["get", "head"]:
        client = httpx.Client()
    elif protocol == "tcp":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif protocol == "udp":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        print(Fore.RED + f"Invalid protocol: {protocol}" + Style.RESET_ALL)
        return

    start_time = time.time()
    if thread_id == 0:
        if protocol in ["get", "head", "cfb"]:
            print(Fore.YELLOW + f"Stressing started on {url} successfully!" + Style.RESET_ALL)
        elif protocol in ["tcp", "udp"]:
            print(Fore.YELLOW + f"Stressing started on {ip}:{port} successfully!" + Style.RESET_ALL)
    while time.time() - start_time < duration:
        if protocol in ["get", "head", "cfb"]:
            send_request(client)
        elif protocol in ["tcp", "udp"]:
            send_packet(sock)
    if thread_id == 0:
        print(Fore.YELLOW + "Stress test ended." + Style.RESET_ALL)

def send_request(client):
    try:
        if protocol == "get":
            response = client.get(url)
        elif protocol == "head":
            response = client.head(url)
    except Exception as e:
        pass # Suppress error messages

def send_packet(sock):
    try:
        if protocol == "tcp":
            sock.connect((ip, port))
            sock.send(b"Stress test packet")
            sock.close()
        elif protocol == "udp":
            sock.sendto(b"Stress test packet", (ip, port))
    except Exception as e:
        pass # Suppress error messages

# Create and start the threads
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=stress_test, args=(i,))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()
