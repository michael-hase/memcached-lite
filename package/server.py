import socket
import threading
import yaml
import os

# Load server config file
with open('package/config/settings.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

HOST = config['server']['host']
PORT = config['server']['port']
STORAGE_FILE = 'data/storage.yaml'

# Ensure data directory exists
os.makedirs(os.path.dirname(STORAGE_FILE), exist_ok=True)

data_store = {}

# Load data from storage file if exists
if os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, 'r') as f:
        data_store = yaml.safe_load(f) or {}


def save_data():
    """Save the data store to a file (YAML format)."""
    with open(STORAGE_FILE, 'w') as f:
        yaml.dump(data_store, f)


def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8').strip()
            if not data:
                break

            parts = data.split()
            command = parts[0]

            if command == 'get':
                # Implementation for 'get' command
                key = parts[1]
                value = data_store.get(key, None)
                if value is not None:
                    response = f"VALUE {key} 0 {len(value)}\r\n{value}\r\nEND\r\n"
                else:
                    response = "END\r\n"
                client_socket.sendall(response.encode('utf-8'))

            elif command == 'set':
                # Implementation for 'set' command
                if len(parts) >= 5:
                    key, flags, exptime, bytes_length = parts[1], parts[2], parts[3], parts[4]
                    data_block = client_socket.recv(int(bytes_length) + 2)
                    data_block = data_block.decode('utf-8').rstrip('\r\n')
                    data_store[key] = data_block
                    save_data()
                    client_socket.sendall(b"STORED\r\n")
                else:
                    client_socket.sendall(b"ERROR\r\n")

            else:
                client_socket.sendall(b"ERROR\r\n")

        except Exception as e:
            print(f"Error: {e}")
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


if __name__ == '__main__':
    start_server()
