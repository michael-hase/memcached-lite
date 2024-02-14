import socket
import time

HOST = '127.0.0.1'  # Server IP
PORT = 11211     # Server port
NUM_OPERATIONS = 100  # Number of operations for testing


def measure_operation(operation, key, value=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        start_time = time.time()
        if operation == 'set':
            s.sendall(f'set {key} {len(value)}\r\n{value}\r\n'.encode())
        elif operation == 'get':
            s.sendall(f'get {key}\r\n'.encode())
        response = s.recv(1024)
        end_time = time.time()
    return end_time - start_time, response


# Measure SET operations
set_times = []
for i in range(NUM_OPERATIONS):
    key, value = f'key_{i}', f'value_{i}'
    duration, _ = measure_operation('set', key, value)
    set_times.append(duration)

# Measure GET operations
get_times = []
for i in range(NUM_OPERATIONS):
    key = f'key_{i}'
    duration, _ = measure_operation('get', key)
    get_times.append(duration)

print(f"Average SET latency: {sum(set_times) / len(set_times)} seconds")
print(f"Average GET latency: {sum(get_times) / len(get_times)} seconds")
