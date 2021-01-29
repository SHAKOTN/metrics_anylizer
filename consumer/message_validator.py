import json
import logging
from typing import Dict

logger = logging.getLogger(__name__)


REQUIRED_MESSAGE_POINTS = [
    'alarmCategory',
    'alarmGroup',
    'alarmCSN',
    'alarmID',
    'alarmMO',
    'alarmNotificationType',
    'alarmLastSeqNo',
    'alarmEventTime',
    'vnocAlarmID'
]


def is_valid_consumer_message(consumer_message: Dict) -> bool:
    is_valid = True
    dumped_message = json.loads(consumer_message['metadata'])
    if not all(key in dumped_message.keys() for key in REQUIRED_MESSAGE_POINTS):
        logger.error(
            f"Message required to contain {REQUIRED_MESSAGE_POINTS} keys. "
            f"Received {dumped_message.keys()} instead"
        )
        is_valid = False
    return is_valid
