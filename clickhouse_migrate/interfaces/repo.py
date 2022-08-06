from typing import List

from clickhouse_migrate.common.db import execute, execute_for_replicas
from clickhouse_migrate.models.migration import MigrationMeta


class MigrationRepo:
    @staticmethod
    def init_migration_table():
        """
        Method for migration initialization
        It creates table to store info about applied migrations
        """
        execute_for_replicas(
            """
                create table if not exists clickhouse_migrate (
                    migration_id String,
                    migration_hash String,
                    filename String,
                    applyed_at DateTime default now()
                )
                engine = MergeTree order by tuple(applyed_at);
            """
        )

    @classmethod
    def apply_migration(cls, sql: str, replicated: bool, migration_meta: MigrationMeta):
        """
        Apply migration for several replicas or for only one db
        :param sql: Migration step sql that should be applied
        :param replicated: Boolean parameter which indicates if the provided sql should be executed
        on each of the provided datrabase instances or not
        :param migration_meta: Meta that has to be written to the migrate table
        """
        if replicated:
            execute_for_replicas(query=sql)
        else:
            execute(query=sql)
        cls.insert_applied_migration_version(migration_meta=migration_meta)

    @staticmethod
    def insert_applied_migration_version(migration_meta: MigrationMeta):
        query = """
            insert into clickhouse_migrate (migration_id, migration_hash, filename)
            values (%(migration_id)s, %(migration_hash)s, %(filename)s)
        """
        execute_for_replicas(query=query, params=migration_meta.asdict())

    @staticmethod
    def get_applied_migrations() -> List[MigrationMeta]:
        query = """
            select migration_id, migration_hash, filename from clickhouse_migrate
        """
        return [
            MigrationMeta(migration_id=record[0], migration_hash=record[1], filename=record[2])
            for record in execute(query=query)
        ]
