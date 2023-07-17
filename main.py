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

if __name__ == "__main__":
    url = input("Enter website URL (including http:// or https://): ")
    num_threads = int(input("Enter number of threads to use: "))
    duration = int(input("Enter duration of stress test in seconds: "))
    until_datetime = time() + duration
    scraper = cloudscraper.create_scraper()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(send_request, url, until_datetime, scraper)
