from dataclasses import dataclass

from clickhouse_driver.dbapi.connection import Connection


@dataclass(frozen=True)
class Database:
    connection: Connection
    is_in_cluster: bool
    cluster_name: str
