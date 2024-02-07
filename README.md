# memcached-lite

This project implements a simplified version of a Memcached-like server in Python. It is designed to handle basic `get` and `set` operations with persistence and introduces a small random delay in processing to simulate real-world scenarios.

## Features

- **Basic Key-Value Store**: Implements fundamental `get` and `set` operations similar to Memcached.
- **Data Persistence**: Stores data in YAML format on disk to ensure persistence across server restarts.
- **Random Operation Delay**: Introduces a random delay for each operation to simulate network or processing latencies.
- **Threaded Server**: Handles multiple client connections concurrently using threads.

## Getting Started

### Prerequisites

- Python 3.6 or later
- PyYAML library

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://your-repository-url/memcached-lite.git
   cd memcached-lite
   ```
## Installation

**Install required Python packages:**

```sh
pip install -r requirements.txt
```

## Running the Server

1. **Navigate to the project directory.**

2. **Start the server by running:**

```sh
python package/server.py
```
This will start the server on the configured host and port defined in package/config/settings.yaml.

## Connecting with the Client

1. Open another terminal window.

2. Run the client script:

```sh
python package/client.py
```

You can now use get and set commands to interact with the server. For example:

```sh
Enter command: set testkey 0 0 4
Enter data block: test
```
```sh
Enter command: get testkey
```
To exit the client, type quit.

## Configuration

Server configurations such as host, port, and storage file path can be adjusted in the `package/config/settings.yaml` file.

## Testing

The tests directory contains test scripts to validate the functionality of the server. Run the tests using:

```sh
python -m unittest discover tests
```
