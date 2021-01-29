import logging
import os
from typing import Any
from typing import Iterable
from typing import Optional
from typing import Tuple
from typing import List

import psycopg2

logger = logging.getLogger(__name__)


class Session:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def fetch_all(self, sql: str, values: Optional[Iterable[Any]] = None) -> List[Tuple[Any]]:
        self.execute(sql, values)
        return self._cursor.fetchall()

    def fetch_one(self, sql: str, values: Optional[Iterable[Any]] = None) -> Tuple[Any]:
        self.execute(sql, values)
        return self._cursor.fetchone()

    def execute(self, sql: str, values: Optional[Iterable[Any]] = None) -> None:
        self._cursor.execute(sql, values)

    def commit(self) -> None:
        self._connection.commit()

    def __enter__(self) -> "Session":
        if not self._connection:
            self._connect()
        return self

    def __exit__(self, exception_type, exception_value, trace) -> None:
        if exception_type is not None:
            logger.error(f"DB exception: {exception_value}")
        self._connection.close()
        self._cursor.close()

    def _connect(self) -> None:
        self._connection = psycopg2.connect(
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST', 'db'),
            port=os.getenv('POSTGRES_PORT', 5432),
        )
        self._cursor = self._connection.cursor()
