import json
import logging
import os
import threading

from kafka import KafkaConsumer

from consumer.constants import KAFKA_TOPIC
from consumer.constants import KAFKA_HOST
from consumer.database import Session
from consumer.message_validator import is_valid_consumer_message

logger = logging.getLogger(__name__)


def consume_messages() -> None:
    logger.warning(f"Started listener {threading.get_ident()}")
    kafka_consumer = KafkaConsumer(
        os.getenv(KAFKA_TOPIC, 'metrics'),
        bootstrap_servers=os.getenv(KAFKA_HOST, ['kafka:9092']),
        enable_auto_commit=True,
        value_deserializer=lambda data: json.loads(data.decode('utf8')),
    )

    with Session() as session:
        for message in kafka_consumer:
            if not is_valid_consumer_message(message.value):
                logger.warning(f"Received invalid message: {message.value}")
                continue
            metadata = json.loads(message.value['metadata'])
            session.execute(
                """
                INSERT INTO metrics(
                    affected_node, affected_equipment, affected_site, alarm_category,
                    alarm_group, alarm_csn, alarm_id, alarm_mo, alarm_notification_type,
                    alarm_last_seq_no, alarm_event_time, vnoc_alarm_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    metadata.get('affectedNode'),
                    metadata.get('affectedEquipment'),
                    metadata.get('affectedSite'),
                    metadata['alarmCategory'],
                    metadata['alarmGroup'],
                    metadata['alarmCSN'],
                    metadata['alarmID'],
                    metadata['alarmMO'],
                    metadata['alarmNotificationType'],
                    metadata['alarmLastSeqNo'],
                    metadata['alarmEventTime'],
                    metadata['vnocAlarmID'],
                ))
            session.commit()
