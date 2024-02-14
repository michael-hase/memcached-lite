import socket
import time
import yaml

# Load server config file
with open('package/config/settings.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

HOST = config['server']['host']
PORT = config['server']['port']


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


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            print("Connected to server.")

            # Add a delay after connecting
            time.sleep(1)

            for i in range(5):
                key = f"key_{i}"
                value = f"value_{i}"

                # Set request
                set_command = f"set {key} {len(value)}\r\n"
                send_command(sock, set_command, value + '\r\n')

                # Small delay
                time.sleep(0.5)

                # Get request
                get_command = f"get {key}\r\n"
                send_command(sock, get_command)

    except KeyboardInterrupt:
        print("\nClient exiting.")
    except Exception as e:
        print(f"Connection error: {e}")


if __name__ == '__main__':
    main()
