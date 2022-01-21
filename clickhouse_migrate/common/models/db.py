from dataclasses import dataclass
from typing import Iterable

from clickhouse_driver.dbapi.connection import Connection


@dataclass(frozen=True)
class Database:
    connection: Connection


@dataclass(frozen=True)
class ReplicaSet:
    replicas: Iterable[Database]
    connection: Connection
