import threading
import requests

def send_request(url):
    while True:
        try:
            response = requests.get(url)
            print(f"Status code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    url = "https://www.yourwebsite.com"
    num_threads = 10
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=send_request, args=(url,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
