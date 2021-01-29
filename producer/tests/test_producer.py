from unittest.mock import MagicMock

from producer.metrics_generator import read_metrics
from producer.producer import send


def test_message_send():
    producer_mock = MagicMock()
    send(producer_mock)
    # Number of calls eq to number of metrics
    assert producer_mock.send.call_count == len(read_metrics())
