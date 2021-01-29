import json
import logging
import os
import threading
from time import sleep

from kafka import KafkaProducer

from producer.constants import KAFKA_HOST
from producer.constants import KAFKA_TOPIC
from producer.metrics_generator import read_metrics

logger = logging.getLogger(__name__)


def produce_messages() -> None:
    logger.warning(f"Started producer {threading.get_ident()}")
    kafka_producer = KafkaProducer(
        bootstrap_servers=os.getenv(KAFKA_HOST, ['kafka:9092']),
        value_serializer=lambda data: json.dumps(data).encode('utf-8')
    )
    while True:
        send(kafka_producer)
        sleep(360)


def send(transport: KafkaProducer) -> None:
    metrics = read_metrics()
    for metric in metrics:
        logger.warning(f"Sending message with data: {metric}")
        transport.send(os.getenv(KAFKA_TOPIC, 'metrics'), value=metric)
