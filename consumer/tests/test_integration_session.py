import pytest
from psycopg2 import InterfaceError

from consumer.database import Session


def test_raises_cursor_already_closed(migrate_table):
    with Session() as session:
        pass
    with pytest.raises(InterfaceError):
        session.execute("SELECT * FROM metrics ORDER BY alarm_event_time DESC;")


def test_raises_invalid_sql(migrate_table):
    with pytest.raises(Exception):
        with Session() as session:
            session.execute(
                "INSERT INSERT INTO metrics(url, content, response_time, code) VALUES (%s, %s, %s, %s)",
                ("http://github.com", "another on", 3.33, 201)
            )


def test_raises_insert_invalid_type(migrate_table):
    with pytest.raises(Exception):
        with Session() as session:
            session.execute(
                """
                INSERT INTO metrics(
                    affected_node, affected_equipment, affected_site, alarm_category,
                    alarm_grou, alarm_csn, alarm_id, alarm_mo, alarm_notification_type,
                    alarm_last_seq_no, alarm_event_time, vnoc_alarm_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    "something", "something", "something", "something", "something", "something"
                    "something", "something", "something", "something", "something", "something"
                )
            )


def test_fetch_all(populate_table_with_test_data):
    select_sql = "SELECT vnoc_alarm_id FROM metrics ORDER BY alarm_event_time DESC;"
    with Session() as session:
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
                "015",
            ))
        session.commit()
        select_results = session.fetch_all(select_sql)

    assert select_results == [('005',), ('005',), ('005',), ('015',)]


def test_fetch_one(populate_table_with_test_data):
    select_sql = "SELECT vnoc_alarm_id FROM metrics ORDER BY alarm_event_time DESC;"

    with Session() as session:
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
                "2020-01-29T09:19:50+02:00",
                "015",
            ))
        session.commit()
        select_results = session.fetch_one(select_sql)

    assert select_results == ('015',)
