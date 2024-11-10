# producers/create_topics.py
import yaml
from confluent_kafka.admin import AdminClient, NewTopic, KafkaError

def load_kafka_config(filepath="config/kafka_config.yaml"):
    with open(filepath, "r") as file:
        return yaml.safe_load(file)

def load_confluent_config(filepath="config/confluent_cloud_config.yaml"):
    with open(filepath, "r") as file:
        return yaml.safe_load(file)

def create_topics():
    kafka_config = load_kafka_config()
    confluent_config = load_confluent_config()

    admin_config = {
        'bootstrap.servers': confluent_config['bootstrap_servers'],
        'security.protocol': confluent_config['security_protocol'],
        'sasl.mechanism': confluent_config['sasl_mechanisms'],
        'sasl.username': confluent_config['sasl_username'],
        'sasl.password': confluent_config['sasl_password']
    }

    admin_client = AdminClient(admin_config)

    topics_to_create = []
    for topic in kafka_config['topics']:
        new_topic = NewTopic(
            topic['name'],
            num_partitions=topic['partitions'],
            replication_factor=topic['replication_factor']
        )
        topics_to_create.append(new_topic)

    futures = admin_client.create_topics(topics_to_create)

    for topic, future in futures.items():
        try:
            future.result()
            print(f"Topic '{topic}' created successfully.")
        except Exception as e:
            if isinstance(e.args[0], KafkaError) and e.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
                print(f"Topic '{topic}' already exists.")
            else:
                print(f"Failed to create topic '{topic}': {e}")

if __name__ == "__main__":
    create_topics()
