from datetime import datetime

from consumer.histogram import _timeline_era015

from consumer.histogram import _most_affected_nodes

from consumer.database import Session
from consumer.histogram import _most_frequent_histogram


def test_most_frequent_histo(populate_table_with_test_data):
    most_frequent = _most_frequent_histogram()
    assert most_frequent == [('9175147', 3)]  # alarm_id, count of alarms

    # Add two more entities
    with Session() as session:
        for i in range(2):
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
                    "9175144",
                    "SubNetwork=Zagreb,MeContext=LX00015,ManagedElement=LX00015bleUnit=RRU-B1B3-S1-2",
                    "Minor",
                    "1460077",
                    "2020-01-24T09:19:50+02:00",
                    "ERA005",
                ))
        session.commit()
    assert _most_frequent_histogram() == [('9175147', 3), ('9175144', 2)]


def test_most_affected_nodes_histo(populate_table_with_test_data):
    most_frequent = _most_affected_nodes()
    assert most_frequent == [('LX00018', 3)]  # node_id, times affected

    # Add two more entities
    with Session() as session:
        for i in range(2):
            session.execute(
                """
                INSERT INTO metrics(
                    affected_node, affected_equipment, affected_site, alarm_category,
                    alarm_group, alarm_csn, alarm_id, alarm_mo, alarm_notification_type,
                    alarm_last_seq_no, alarm_event_time, vnoc_alarm_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    "LX00012",
                    "RRU-B1B3-S1-2",
                    "LX00012",
                    "FAULT",
                    "003--1143982548-SubNetwork=Zagreb,MeContext=LX00015,ManagedElement=LX00015",
                    "1460077",
                    "9175144",
                    "SubNetwork=Zagreb,MeContext=LX00015,ManagedElement=LX00015bleUnit=RRU-B1B3-S1-2",
                    "Minor",
                    "1460077",
                    "2020-01-24T09:19:50+02:00",
                    "ERA005",
                ))
        session.commit()

    most_frequent = _most_affected_nodes()
    assert most_frequent == [('LX00018', 3), ('LX00012', 2)]


def test_era015_timeline(populate_table_with_test_data):
    era_timeline = _timeline_era015()

    assert era_timeline == [(datetime(2020, 1, 24, 9), 3)]  # grouped date by hour, count of entities created

    # Add two more entities
    with Session() as session:
        for i in range(2):
            session.execute(
                """
                INSERT INTO metrics(
                    affected_node, affected_equipment, affected_site, alarm_category,
                    alarm_group, alarm_csn, alarm_id, alarm_mo, alarm_notification_type,
                    alarm_last_seq_no, alarm_event_time, vnoc_alarm_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    "LX00012",
                    "RRU-B1B3-S1-2",
                    "LX00012",
                    "FAULT",
                    "003--1143982548-SubNetwork=Zagreb,MeContext=LX00015,ManagedElement=LX00015",
                    "1460077",
                    "9175144",
                    "SubNetwork=Zagreb,MeContext=LX00015,ManagedElement=LX00015bleUnit=RRU-B1B3-S1-2",
                    "Minor",
                    "1460077",
                    "2020-01-22T09:19:50+02:00",
                    "ERA005",
                ))
        session.commit()

    era_timeline = _timeline_era015()

    assert era_timeline == [(datetime(2020, 1, 24, 9), 3), (datetime(2020, 1, 22, 9), 2)]
