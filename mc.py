import asyncio
import socket

async def connect_to_server():
    server_address = ('185.107.193.2', 37513)  # Replace with your server IP and port
    num_connections = 10000  # Number of connections to simulate
    connection_timeout = 5  # Timeout for connecting to the server in seconds

    for _ in range(num_connections):
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(*server_address),
                timeout=connection_timeout
            )
            print("Connected to the server successfully!")
            writer.close()
            await writer.wait_closed()
        except (socket.gaierror, asyncio.TimeoutError):
            print("Failed to connect to the server.")

async def main():
    await asyncio.gather(*[connect_to_server() for _ in range(100)])  # Simulate 10 threads making connections

if __name__ == "__main__":
    asyncio.run(main())
