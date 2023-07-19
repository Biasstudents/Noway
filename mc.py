import socket

# Set the server IP address and port number
server_ip = '185.107.194.87'
server_port = 60184

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
sock.connect((server_ip, server_port))

# Send data to the server (replace with your own data)
data = b'Hello, server!'
sock.sendall(data)

# Receive data from the server
response = sock.recv(1024)

# Close the connection
sock.close()

# Print the response from the server
print('Received:', response)
