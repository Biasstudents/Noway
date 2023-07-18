import cloudscraper
import threading
import time
from termcolor import colored

# Set the number of threads to use
num_threads = int(input("Enter the number of threads to use: "))

# Set the URL of the website to test
url = input("Enter the website URL (including http or https): ")

# Set the duration of the stress test in seconds
duration = int(input("Enter the duration of the stress test in seconds: "))

# Set the interval for checking the website status in seconds
status_interval = 10

def stress_test():
    scraper = cloudscraper.create_scraper()
    start_time = time.time()
    print(colored(f"Stress test started on {url} successfully!", "blue"))
    while time.time() - start_time < duration:
        send_request(scraper)
        time.sleep(status_interval)
        check_status(scraper)
    print(colored("Stress test ended.", "blue"))

def send_request(scraper):
    response = scraper.get(url)

def check_status(scraper):
    try:
        response = scraper.get(url)
        if response.status_code == 200:
            print(colored(f"{url} is online", "green"))
        else:
            print(colored(f"{url} is offline", "red"))
    except:
        print(colored(f"{url} is offline", "red"))

# Create and start the threads
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=stress_test)
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()
