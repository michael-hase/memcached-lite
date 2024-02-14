import socket
import yaml
import random
import time

# Load client configuration
with open('package/config/settings.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

HOST = config['server']['host']
PORT = config['server']['port']


def send_command(sock, command, data=None, data_store=None):
    try:
        # Check if the command is a set command and check for duplicate keys
        if command.lower().startswith('set') and data_store:
            parts = command.split()
            if len(parts) != 4:
                print("Invalid set command format.")
                return

            key = parts[1]
            if key in data_store:
                print("Error: Key already exists in the data store.")
                return

        sock.sendall(command.encode('utf-8'))

        if data:
            sock.sendall(data.encode('utf-8'))

        response = sock.recv(1024).decode('utf-8')
        print("Server response:", response)
    except Exception as e:
        print(f"Error sending command: {e}")


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Introduce a small random delay
            time.sleep(random.uniform(0, 1))  # Sleep for up to 1 second

            sock.connect((HOST, PORT))
            print("Connected to server. Type 'quit' to exit.")

            while True:
                command = input("Enter command ('set <key> <bytes> \\r\\n' or 'get <key>'): ").strip()
                if command.lower() == 'quit':
                    break

                if command.lower().startswith('set'):
                    parts = command.split()
                    if len(parts) != 4:
                        print("Invalid set command format.")
                        continue

                    key, value_size = parts[1], parts[2]
                    value = input("Enter value: ").strip()

                    if len(value) != int(value_size):
                        print(f"Value size does not match specified size.")
                        continue

                    set_command = f"set {key} {value_size}\r\n"
                    send_command(sock, set_command, value + '\r\n')

                elif command.lower().startswith('get'):
                    parts = command.split()
                    if len(parts) != 2:
                        print("Invalid get command format.")
                        continue

                    send_command(sock, command)

                else:
                    print("Invalid command.")

    except KeyboardInterrupt:
        print("\nClient exiting.")
    except Exception as e:
        print(f"Connection error: {e}")


if __name__ == '__main__':
    main()
