import cloudscraper
import threading
import time
from colorama import Fore, Style, init

# Initialize colorama
init()

# Set the URL of the website to test
url = input("Enter the website URL (including http or https): ")

# Set the number of threads to use
num_threads = int(input("Enter the number of threads to use: "))

# Set the duration of the stress test in seconds
duration = int(input("Enter the duration of the stress test in seconds: "))

# Set the interval for checking the website status in seconds
status_interval = 10

def stress_test(thread_id):
    scraper = cloudscraper.create_scraper()
    start_time = time.time()
    if thread_id == 0:
        print(Fore.YELLOW + f"Stressing started on {url} successfully!" + Style.RESET_ALL)
    while time.time() - start_time < duration:
        send_request(scraper)
        if thread_id == 0:
            time.sleep(status_interval)
            check_status(scraper)
    if thread_id == 0:
        print(Fore.YELLOW + "Stress test ended." + Style.RESET_ALL)

def send_request(scraper):
    try:
        response = scraper.get(url)
    except Exception as e:
        print(f"Error sending request: {e}")


def check_status(scraper):
    try:
        start_time = time.time()
        response = scraper.get(url)
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
    thread.join(
