from dataclasses import dataclass

from clickhouse_migrate.common.models.base import BaseDto


@dataclass(frozen=True)
class Step:
    sql: str
    replicated: bool = True


@dataclass
class MigrationMeta(BaseDto):
    migration_id: str
    migration_hash: str
    filename: str
