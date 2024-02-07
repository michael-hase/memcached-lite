import unittest
from package import client


class TestClient(unittest.TestCase):
    def test_send_command(self):
        # Test sending a command using the client and receiving a response
        # This is a conceptual test; you might need to adjust it based on your client implementation
        response = client.send_command('get testkey\r\n')
        self.assertTrue('Test' in response)


if __name__ == '__main__':
    unittest.main()
