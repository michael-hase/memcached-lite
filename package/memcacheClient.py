import yaml
from pymemcache.client import base

# Load server configuration from settings.yaml
with open('config/settings.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Extract host and port from the loaded configuration
host = config['server']['host']
port = config['server']['port']

# Create a PyMemcache client using the host and port from settings.yaml
client = base.Client((host, port))

# Set a value
client.set('some_key', 'some value')

# Get the value back
value = client.get('some_key')
print(value)  # Should print 'some value'

# Close the client connection
client.close()
