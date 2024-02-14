import threading
import socket
import time

# Define the server address and port
SERVER_ADDRESS = ('127.0.0.1', 11211)

# Number of clients to simulate
NUM_CLIENTS = 50

# Delay in seconds before each client connects
CONNECTION_DELAY = 1


def send_command(sock, command, data=None):
    try:
        # Print the command
        print("Sending command:", command.strip())

        sock.sendall(command.encode('utf-8'))

        if data:
            sock.sendall(data.encode('utf-8'))

        response = sock.recv(1024).decode('utf-8')
        print("Server response:", response)

    except Exception as e:
        print(f"Error sending command: {e}")


# Function to simulate a client setting a key
def set_key(client_id):
    try:
        time.sleep(CONNECTION_DELAY)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(SERVER_ADDRESS)
            time.sleep(1)
            key = f"conc-Test_{client_id}"
            value = f"lots of clients {client_id}"

            # Set request
            set_command = f"set {key} {len(value)}\r\n"
            send_command(sock, set_command, value + '\r\n')

    except Exception as e:
        print(f"Client {client_id}: Error - {e}")


# Function to simulate a client getting a key
def get_key(client_id):
    try:
        time.sleep(CONNECTION_DELAY)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(SERVER_ADDRESS)
            key = f"conc-Test_{client_id}"
            command = f"get {key}\r\n"
            sock.sendall(command.encode())
            response = sock.recv(1024).decode()
            print(f"Client {client_id}: {response.strip()}")
    except Exception as e:
        print(f"Client {client_id}: Error - {e}")


# Create and start threads for each client
threads = []
for i in range(NUM_CLIENTS):
    thread = threading.Thread(target=set_key, args=(i,))
    threads.append(thread)
    thread.start()

for i in range(NUM_CLIENTS):
    thread = threading.Thread(target=get_key, args=(i,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()
