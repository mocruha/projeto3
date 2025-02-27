import datetime
import io
from time import sleep

from confluent_kafka import Consumer, KafkaError
import boto3

# Constants
BROKER = 'localhost:9094'
TOPIC = 'cpu.public.test_table'
CONSUMER_CONFIG = {
    'bootstrap.servers': BROKER,
    'group.id': 'cpu_group',
    'auto.offset.reset': 'earliest'
}
AWS_ACCESS_KEY = 'alcantara'
AWS_SECRET_KEY = 'senhasegura'
AWS_BUCKET_NAME = 'baldinho'
AWS_REGION = 'us-east-1'

MINIO_ENDPOINT = 'localhost:9000'


def consume_messages():
    """Consume messages from Kafka and write them to S3."""
    consumer = Consumer(CONSUMER_CONFIG)
    consumer.subscribe([TOPIC])

    try:
        while True:
            message = consumer.poll(0.5)
            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    continue
                raise KafkaError(message.error())

            print(f"Received message: key={message.key()}")
            s3_put_message(message.value(), message.key().decode())

    except KeyboardInterrupt:
        print("\nConsumer interrupted by user.")
    finally:
        consumer.close()
        print("Consumer closed gracefully.")


def create_s3_client():
    """Create an S3 client using boto3 with MinIO endpoint"""
    s3_client = boto3.client(
        's3',
        endpoint_url=f'http://{MINIO_ENDPOINT}',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
        verify=False
    )
    return s3_client


def s3_put_message(message, name):
    """
    Upload a message to S3.

    Parameters:
    message (bytes): The message to be uploaded.
    name (str): The key name for the S3 object
    """
    try:
        s3_client.put_object(
            Bucket=AWS_BUCKET_NAME,
            Key=f'cpu_data_{name}',
            Body=message,
            ContentType='application/json'
        )
    except Exception as e:
        print(f"Error uploading to S3: {e}")


if __name__ == "__main__":
    s3_client = create_s3_client()
    consume_messages()
