import socket

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 12000))  # Bind to localhost on port 12000

    print("Server is ready to receive")

    try:
        while True:
            message, client_address = server_socket.recvfrom(1024)  # Buffer size is 1024 bytes
            print(f"Received message: {message.decode()} from {client_address}")
            if message.decode() == "PING":
                server_socket.sendto("PONG".encode(), client_address)
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
