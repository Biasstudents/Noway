import cloudscraper
import httpx
import threading
import time
from colorama import Fore, Style, init

# Initialize colorama
init()

# Set the protocol/method to use for sending requests
protocol = input("Enter the protocol/method to use (cfb or get): ")

# Set the URL of the website to test
url = input("Enter the website URL (including http or https): ")

# Set the number of threads to use
num_threads = int(input("Enter the number of threads to use: "))

# Set the duration of the stress test in seconds
duration = int(input("Enter the duration of the stress test in seconds: "))

# Set the interval for checking the website status in seconds
status_interval = 10

def stress_test(thread_id):
    if protocol == "cfb":
        client = cloudscraper.create_scraper()
    elif protocol == "get":
        client = httpx.Client()
    else:
        print(Fore.RED + f"Invalid protocol: {protocol}" + Style.RESET_ALL)
        return

    start_time = time.time()
    if thread_id == 0:
        print(Fore.YELLOW + f"Stressing started on {url} successfully!" + Style.RESET_ALL)
    while time.time() - start_time < duration:
        send_request(client)
        if thread_id == 0:
            time.sleep(status_interval)
            check_status(client)
    if thread_id == 0:
        print(Fore.YELLOW + "Stress test ended." + Style.RESET_ALL)

def send_request(client):
    try:
        response = client.get(url)
    except Exception as e:
        print(f"Error sending request: {e}")

def check_status(client):
    try:
        start_time = time.time()
        response = client.get(url)
        end_time = time.time()
        response_time = end_time - start_time
        if response.status_code == 200:
            print(Fore.GREEN + f"{url} is online (response time: {response_time:.2f} seconds)" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"{url} is offline" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"{url} is offline" + Style.RESET_ALL)

# Create and start the threads
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=stress_test, args=(i,))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()
