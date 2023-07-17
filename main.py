import requests
from concurrent.futures import ThreadPoolExecutor
from time import time

def send_request(url):
    try:
        response = requests.head(url)
        print(f"Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    url = input("Enter website URL (including http:// or https://): ")
    num_threads = int(input("Enter number of threads to use: "))
    duration = int(input("Enter duration of stress test in seconds: "))
    start_time = time()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        while time() - start_time < duration:
            executor.submit(send_request, url)
