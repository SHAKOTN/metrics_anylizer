import logging

from consumer.database.database_session import Session

logger = logging.getLogger(__name__)


def migrate_metrics_table() -> None:
    create_table_query = """
        create table if not exists 
        metrics(
            id serial primary key,  
            created_on timestamp default current_timestamp, 
            affected_node varchar (256),
            affected_equipment varchar (256),
            affected_site varchar (256), 
            alarm_category varchar (100), 
            alarm_group varchar (4096), 
            alarm_csn varchar (100), 
            alarm_id varchar (100), 
            alarm_mo varchar (4096),
            alarm_notification_type varchar (20),
            alarm_last_seq_no varchar (100),
            alarm_event_time timestamp,
            vnoc_alarm_id varchar(100)
        );
    """

    create_index_query = """
        create index if not exists alarm_id_time_node_idx
        on metrics (affected_node, alarm_id, vnoc_alarm_id);
    """
    with Session() as session:
        session.execute(create_table_query)
        session.execute(create_index_query)
        session.commit()


def drop_metrics_table():
    with Session() as session:
        session.execute("drop table if exists metrics;")
        session.execute("drop index if exists alarm_id_time_node_idx;")
        session.commit()


if __name__ == '__main__':
    logger.warning("!!!Migrating database!!!")
    migrate_metrics_table()
