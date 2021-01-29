from unittest.mock import MagicMock
from datetime import datetime
import pytest

from consumer.database import Session
from consumer.database.migrate import drop_metrics_table
from consumer.database.migrate import migrate_metrics_table


@pytest.fixture
def psycopg2_connect_fixture(mocker):
    mocker.patch(
        "consumer.database.database_session.psycopg2.connect",
        return_value=MagicMock()
    )


@pytest.fixture
def psycopg2_session_exception_on_commit(mocker, psycopg2_connect_fixture):
    mocker.patch(
        "consumer.database.database_session.Session.commit",
        side_effect=Exception("")
    )


@pytest.fixture
def migrate_table():
    drop_metrics_table()
    migrate_metrics_table()
    yield
    drop_metrics_table()


@pytest.fixture
def populate_table_with_test_data(migrate_table):
    with Session() as session:
        for i in range(3):
            session.execute(
                """
                INSERT INTO metrics(
                    affected_node, affected_equipment, affected_site, alarm_category,
                    alarm_group, alarm_csn, alarm_id, alarm_mo, alarm_notification_type,
                    alarm_last_seq_no, alarm_event_time, vnoc_alarm_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    "LX00018",
                    "RRU-B1B3-S1-2",
                    "LX00015",
                    "FAULT",
                    "003--1143982548-SubNetwork=Zagreb,MeContext=LX00015,ManagedElement=LX00015",
                    "1460077",
                    "9175147",
                    "SubNetwork=Zagreb,MeContext=LX00015,ManagedElement=LX00015bleUnit=RRU-B1B3-S1-2",
                    "Minor",
                    "1460077",
                    "2020-01-24T09:19:50+02:00",
                    "ERA005",
                ))
        session.commit()


@pytest.fixture
def consumer_mocked(mocker):
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
                    "\"alarmEventTime\":\"2020-01-21T15:45:15+02:00\",\"vnocAlarmID\":\"ERA021\"}"
            }),
        ]
    )


@pytest.fixture
def consumer_mocked_multiple_messages(mocker):
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
                    "\"alarmEventTime\":\"2020-01-21T15:45:15+02:00\",\"vnocAlarmID\":\"ERA021\"}"
            }),
            MagicMock(value={
                "metadata": "{\"affectedNode\":\"LX000232\",\"affectedSite\":\"LX000232\","
                            "\"alarmCategory\":\"FAULT\",\"alarmGroup\":\"003--936265541-SubNetwork=Osijek,"
                            "MeContext=LX000232,ManagedElement=LX000232,ENodeBFunction=1,NbIotCell=platana-1469856\","
                            "\"alarmCSN\":\"1469856\",\"alarmID\":\"9175114\",\"alarmMO\":\"SubNetwork=Osijek,"
                            "MeContext=LX000232,ManagedElement=LX000232,ENodeBFunction=1,NbIotCell=platana\","
                            "\"alarmNotificationType\":\"Major\",\"alarmLastSeqNo\":\"1469856\","
                            "\"alarmEventTime\":\"2020-01-21T15:45:10+02:00\",\"vnocAlarmID\":\"ERA015\"} "
            })
        ]
    )
