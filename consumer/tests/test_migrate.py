from consumer.database import migrate_metrics_table
from consumer.database import drop_metrics_table
from consumer.database import Session


def test_create_table():
    migrate_metrics_table()
    with Session() as session:
        # Check table was created
        result = session.fetch_one("SELECT to_regclass('metrics');")
    assert result == ('metrics',)


def test_create_drop_table():
    migrate_metrics_table()
    drop_metrics_table()
    with Session() as session:
        # Check table was dropped
        result = session.fetch_one("SELECT to_regclass('metrics');")
    assert result == (None,)
