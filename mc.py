import socket
import threading
import time

SERVER_IP = input("Enter the server IP: ")
SERVER_PORT = int(input("Enter the server port: "))

def connect_to_server():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_IP, SERVER_PORT))
            print("Connected to server")
        except:
            print("Failed to connect to server")

NUM_THREADS = int(input("Enter the number of threads: "))
DURATION = int(input("Enter the duration (in seconds): "))

threads = []
for i in range(NUM_THREADS):
    thread = threading.Thread(target=connect_to_server)
    thread.start()
    threads.append(thread)

time.sleep(DURATION)

for thread in threads:
    thread.join()
