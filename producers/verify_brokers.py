import yaml
from confluent_kafka.admin import AdminClient

def load_config(filepath="config/confluent_cloud_config.yaml"):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def verify_brokers():
    config = load_config()

    admin_config = {
        'bootstrap.servers': config['bootstrap_servers'],
        'security.protocol': config['security_protocol'],
        'sasl.mechanism': config['sasl_mechanisms'],
        'sasl.username': config['sasl_username'],
        'sasl.password': config['sasl_password']       
    }

    admin_client = AdminClient(admin_config)
    cluster_metadata = admin_client.list_topics(timeout=10)

    if cluster_metadata.brokers:
        print("Kafka brokers are running successfully:")
        for broker_id, broker in cluster_metadata.brokers.items():
            print(f"Broker ID: {broker_id}, Host: {broker.host}")
        return True
    else:
        print("No brokers found.")
        return False
    
if __name__ == "__main__":
    verify_brokers()