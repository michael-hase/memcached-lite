import socket
import threading
import yaml
import time
import random
import os
import logging
import json
import signal

# Load server config file
with open('package/config/settings.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

HOST = config['server']['host']
PORT = config['server']['port']
STORAGE_FILE = 'data/storage.json'

# Check to make sure data directory exists
os.makedirs(os.path.dirname(STORAGE_FILE), exist_ok=True)


# Load data from storage file if exists
def load_data():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(STORAGE_FILE, 'w') as f:
        json.dump(data, f)


data_store = load_data()
lock = threading.Lock()  # Add a lock for thread-safe access to data_store

# Configure logging
logging.basicConfig(filename='server.log', level=logging.ERROR)


def handle_client(client_socket):
    while True:
        try:
            header = client_socket.recv(1024).decode('utf-8').strip()
            if not header:
                break

            # Introduce a small random delay
            time.sleep(random.uniform(0, 1))  # Sleep for up to 1 second

            parts = header.split()
            command = parts[0]

            if command == 'get':
                key = parts[1]
                with lock:
                    value = data_store.get(key, None)
                if value is not None:
                    response = f"VALUE {key} 0 {len(value)}\r\n{value}\r\nEND\r\n"
                else:
                    response = "END\r\n"
                client_socket.sendall(response.encode('utf-8'))

            elif command == 'set' and len(parts) == 3:
                key, value_size_str = parts[1], parts[2]
                value_size = int(value_size_str)

                # Read value based on the specified size
                value_data = client_socket.recv(value_size).decode('utf-8')

                # Consume the trailing \r\n after the value if needed
                client_socket.recv(2)

                # Check if the key already exists
                if key in data_store:
                    client_socket.sendall(b"NOT-STORED\r\n")
                else:
                    with lock:
                        data_store[key] = value_data
                        save_data(data_store)  # Persist data to the filesystem
                    client_socket.sendall(b"STORED\r\n")

            else:
                client_socket.sendall(b"ERROR\r\n")

        except Exception as e:
            logging.error(f"Error: {e}")  # Log the error
            client_socket.sendall(b"ERROR\r\n")
            break

    client_socket.close()


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server is listening on {HOST}:{PORT}")

        while True:
            client_socket, _ = server_socket.accept()
            print(f"Accepted connection from {client_socket.getpeername()}")
            threading.Thread(target=handle_client, args=(client_socket,)).start()


def save_storage_on_shutdown(sig, frame):
    try:
        save_data(data_store)
        print("Storage saved. Server shutting down.")
        exit(0)
    except Exception as e:
        print(f"Error saving storage: {e}")
        exit(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, save_storage_on_shutdown)
    start_server()
