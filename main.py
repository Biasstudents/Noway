import requests
import threading

url = 'https://tls.mrrage.xyz/nginx_status'
num_threads = 1000

def stress_test():
    while True:
        response = requests.get(url)
        print(response.status_code)

threads = []
for i in range(num_threads):
    t = threading.Thread(target=stress_test)
    t.start()
    threads.append(t)

for t in threads:
    t.join()
