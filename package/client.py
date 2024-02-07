import socket
import yaml

# Load client configuration
with open('package/config/settings.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

HOST = config['server']['host']
PORT = config['server']['port']


def send_command(sock, command, data=None):
    sock.sendall(command.encode('utf-8'))

    # Check if there is a data block to send
    if data:
        # Send the data block followed by \r\n
        sock.sendall(data.encode('utf-8'))
        sock.sendall(b'\r\n')

    response = sock.recv(1024).decode('utf-8')
    print(response)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print("Connected to server. Type your commands below.")

        while True:
            try:
                command = input("Enter command: ")
                if command.lower() == 'quit':
                    break

                if not command.endswith('\r\n'):
                    command += '\r\n'

                data_block = None
                # Check if the command is a 'set' command
                if command.startswith('set'):
                    # Prompt for the data block
                    data_block = input("Enter data block: ")

                send_command(sock, command, data_block)

            except KeyboardInterrupt:
                print("\nClient exiting.")
                break
            except Exception as e:
                print(f"Error: {e}")
                break


if __name__ == '__main__':
    main()
