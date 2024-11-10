import yaml
from confluent_kafka import Producer

def load_config(filepath="config/confluent_cloud_config.yaml"):
    with open(filepath, "r") as file:
        return yaml.safe_load(file)

def check_ssl_connection():
    config = load_config()
    
    producer_config = {
        'bootstrap.servers': config['bootstrap_servers'],
        'security.protocol': config['security_protocol'],
        'sasl.mechanism': config['sasl_mechanisms'],
        'sasl.username': config['sasl_username'],
        'sasl.password': config['sasl_password']
    }

    try:
        producer = Producer(producer_config)
        producer.produce("test-topic", key="test-key", value="test-message")
        producer.flush()
        print("Secure connection established successfully.")
        return True
    except Exception as e:
        print(f"Failed to establish secure connection: {e}")
        return False

if __name__ == "__main__":
    check_ssl_connection()