import unittest
import socket
from package import server


class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This method could be used to start the server in a separate thread
        # For simplicity, we're assuming the server is already running
        pass

    def test_set_get_command(self):
        # Test setting and getting a value from the server
        host, port = "127.0.0.1", 11211  # Should match your server config

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall(b'set testkey 0 0 4\r\nTest\r\n')
            response = sock.recv(1024)
            self.assertIn(b'STORED', response)

            sock.sendall(b'get testkey\r\n')
            response = sock.recv(1024)
            self.assertIn(b'Test', response)

    @classmethod
    def tearDownClass(cls):
        # This method could be used to stop the server if it was started by the test
        pass


if __name__ == '__main__':
    unittest.main()
