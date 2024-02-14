import socket
import threading
import time

HOST = '127.0.0.1'  # Server IP
PORT = 11211     # Server port
NUM_CLIENTS = [10, 20, 50, 100]  # Levels of concurrency to test
TEST_DURATION = 10  # Duration of each test in seconds


def client_workload():
    end_time = time.time() + TEST_DURATION
    while time.time() < end_time:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(b'get some_key\r\n')  # Use a key known to exist
                _ = s.recv(1024)
        except Exception as e:
            print(f"Error in client workload: {e}")


for num_clients in NUM_CLIENTS:
    threads = [threading.Thread(target=client_workload) for _ in range(num_clients)]
    start_time = time.time()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    total_operations = num_clients * (TEST_DURATION / (time.time() - start_time))
    print(f"{num_clients} clients: Throughput = {total_operations} operations/second")
