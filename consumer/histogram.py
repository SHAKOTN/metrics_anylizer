"""
* Histogram about the most frequent alarms
* Histogram about the nodes that got the most alarms
* Timeline about the ERA015 alarms per hour
"""
from typing import Any
from typing import List
from typing import Tuple

from beautifultable import BeautifulTable

from consumer.database import Session


def build_histograms():

    _most_frequent_histogram()
    _most_affected_nodes()
    _timeline_era015()


def _most_frequent_histogram() -> List[Tuple[Any]]:
    with Session() as session:
        alert_counts = session.fetch_all(
            """
            SELECT alarm_id, COUNT(alarm_id) 
            FROM metrics
            GROUP BY alarm_id
            ORDER BY COUNT(alarm_id) DESC;
            """
        )
    table = BeautifulTable()
    print("Most Frequent Alerts")
    for alert in alert_counts:
        table.rows.append([alert[0], alert[1]])
    table.columns.header = ["alert id", "alert count"]
    print(table)
    return alert_counts


def _most_affected_nodes() -> List[Tuple[Any]]:
    top_affected_nodes = 5
    with Session() as session:
        node_counts = session.fetch_all(
            f"""
            SELECT affected_node, COUNT(affected_node) 
            FROM metrics
            GROUP BY affected_node
            ORDER BY COUNT(affected_node) DESC
            LIMIT {top_affected_nodes};
            """
        )
    table = BeautifulTable()
    print(f"Top {top_affected_nodes} most affected nodes")
    for node in node_counts:
        table.rows.append([node[0], node[1]])
    table.columns.header = ["node", "times affected"]
    print(table)
    return node_counts


def _timeline_era015() -> List[Tuple[Any]]:
    with Session() as session:
        era015_timeline = session.fetch_all(
            """
            SELECT date_trunc('hour', alarm_event_time), count(1)
            FROM metrics
            GROUP BY 1
            ORDER BY date_trunc('hour', alarm_event_time) DESC
            """
        )

    table = BeautifulTable()
    print("ERA015 generated per hour")
    for era015_daily in era015_timeline:
        table.rows.append([f"{era015_daily[0]}", era015_daily[1]])

    table.columns.header = ["date", "count"]
    print(table)
    return era015_timeline
