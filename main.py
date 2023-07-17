import cloudscraper
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time, sleep
from threading import Lock

def send_request(url):
    try:
        scraper = cloudscraper.create_scraper()
        start_time = time()
        response = scraper.head(url)
        response_time = time() - start_time
        return (True, response_time)
    except Exception as e:
        return (False, None)

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

if __name__ == "__main__":
    url = input("Enter website URL (including http:// or https://): ")
    num_threads = int(input("Enter number of threads to use: "))
    duration = int(input("Enter duration of stress test in seconds: "))
    start_time = time()
    print(f"Stressing started on {url} successfully!")
    num_requests_sent = 0
    total_response_time = 0
    lock = Lock()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        while time() - start_time < duration:
            future = executor.submit(send_request, url)
            futures.append(future)
            if int(time() - start_time) % 10 == 0:
                if check_website_status(url):
                    print("Website up")
                else:
                    print("Website down")
                with lock:
                    print(f"Requests sent successfully: {num_requests_sent}")
                    if num_requests_sent > 0:
                        avg_response_time = total_response_time / num_requests_sent
                        print(f"Average response time: {avg_response_time:.2f} seconds")
            sleep(1)
        for future in as_completed(futures):
            success, response_time = future.result()
            with lock:
                if success:
                    num_requests_sent += 1
                    total_response_time += response_time
