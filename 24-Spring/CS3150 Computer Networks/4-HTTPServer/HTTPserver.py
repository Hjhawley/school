import socket
import sys
import os

port = 80  # Default port for HTTP
if len(sys.argv) > 1:
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Invalid port")
        sys.exit(1)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.bind(('', port))  # Bind to all interfaces on the specified port
    server_socket.listen(5)  # Start listening for incoming connections, max 5 queued connections
except OSError as e:
    print(f"Error: {e}")
    sys.exit(1)

def handle_request(connection_socket):
    request = connection_socket.recv(1024).decode('utf-8')  # Read the request
    headers = request.split('\n')
    top_header = headers[0].split()
    method = top_header[0]
    filename = top_header[1].strip('/') if len(top_header) > 1 else 'index.html'

    if method == 'GET':
        try:
            with open(filename, 'rb') as file:
                content = file.read()
                connection_socket.send(b"HTTP/1.1 200 OK\r\n")
                connection_socket.send(f"Content-Length: {len(content)}\r\n".encode())
                connection_socket.send(f"Content-Type: text/html\r\n\r\n".encode())  # Assuming HTML for simplicity
                connection_socket.send(content)
        except FileNotFoundError:
            connection_socket.send(b"HTTP/1.1 404 Not Found\r\n")
            connection_socket.send(b"Content-Type: text/html\r\n\r\n")
            connection_socket.send(b"<html><body><h1>404 Not Found</h1></body></html>")
        finally:
            connection_socket.close()

while True:
    try:
        # Accept a new connection
        client_socket, addr = server_socket.accept()
        handle_request(client_socket)
    except KeyboardInterrupt:
        print("Server is shutting down.")
        break

server_socket.close()