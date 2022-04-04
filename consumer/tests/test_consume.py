from unittest.mock import MagicMock

from consumer.consumer import consume_messages
from consumer.database import Session


def test_consume_message_data_saved_to_db(consumer_mocked, migrate_table):
    consume_messages()
    select_sql = "SELECT vnoc_alarm_id FROM metrics ORDER BY alarm_event_time DESC;"
    count_sql = "SELECT COUNT(*) FROM metrics;"
    with Session() as session:
        select_results = session.fetch_one(select_sql)
        count_result = session.fetch_one(count_sql)

    assert select_results == ('ERA021',)
    assert count_result == (1,)


def test_consume_multiple_messages(migrate_table, consumer_mocked_multiple_messages):
    consume_messages()
    count_sql = "SELECT COUNT(*) FROM metrics;"
    with Session() as session:
        count_result = session.fetch_one(count_sql)
    assert count_result == (2,)

    # Check that messages were created properly
    with Session() as session:
        select_result_era015 = session.fetch_one(
            "SELECT vnoc_alarm_id FROM metrics WHERE vnoc_alarm_id = '015';"
        )
        select_result_era021 = session.fetch_one(
            "SELECT vnoc_alarm_id FROM metrics WHERE vnoc_alarm_id = 'ERA021';"
        )
        select_multiple_results = session.fetch_all(
            "SELECT vnoc_alarm_id FROM metrics ORDER BY alarm_event_time DESC;"
        )
    assert select_result_era015 == ("015",)
    assert select_result_era021 == ("ERA021",)
    assert select_multiple_results == [("ERA021",), ("015",)]


def test_invalid_message_data(migrate_table, mocker):
    """
    Case when one required data point is missing. Message should be not saved to database
    """
    mocker.patch(
        "consumer.consumer.KafkaConsumer",
        return_value=[
            MagicMock(value={
                "metadata":
                    "{\"affectedNode\":\"LX000191\",\"affectedEquipment\":\"RRU-B8-S2\","
                    "\"affectedSite\":\"LX000191\",\"alarmCategory\":\"FAULT\","
                    "\"alarmGroup\":\"003--1143978760-SubNetwork=Rijeka,MeContext=LX000191,"
                    "ManagedElement=LX000191,Equipment=1,FieldReplaceableUnit=RRU-B8-S2,"
                    "RfPort=A-1460123\",\"alarmCSN\":\"1460123\",\"alarmID\":\"0\","
                    "\"alarmMO\":\"SubNetwork=Rijeka,MeContext=LX000191,ManagedElement=LX000191,"
                    "Equipment=1,FieldReplaceableUnit=RRU-B8-S2,RfPort=A\","
                    "\"alarmNotificationType\":\"Minor\",\"alarmLastSeqNo\":\"1460123\","
                    "\"alarmEventTime\":\"2020-01-21T15:45:15+02:00\"}"
            }),
        ]
    )
    consume_messages()
    select_sql = "SELECT COUNT(*) FROM metrics;"
    with Session() as session:
        select_results = session.fetch_one(select_sql)

    # Message is not saved into db because it has invalid format
    assert select_results == (0,)
