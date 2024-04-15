import socket
import time

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12000)
    message = "PING"
    rtts = []

    try:
        for i in range(10):  # Adjust number of pings as needed
            start_time = time.time()
            client_socket.sendto(message.encode(), server_address)
            client_socket.settimeout(2.0)  # Set a timeout for socket operations

            try:
                response, server = client_socket.recvfrom(1024)  # Buffer size is 1024 bytes
                elapsed_time = time.time() - start_time
                rtts.append(elapsed_time)
                print(f"Received {response.decode()} from {server}, RTT = {elapsed_time:.3f} seconds")
            except socket.timeout:
                print("Request timed out")

            time.sleep(1)  # Wait a second between pings
    except KeyboardInterrupt:
        if rtts:
            average_rtt = sum(rtts) / len(rtts)
            print(f"Average RTT: {average_rtt:.3f} seconds")
        else:
            print("No RTTs to average.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
