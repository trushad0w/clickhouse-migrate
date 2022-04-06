from typing import List

from clickhouse_migrate.common.db import execute_for_replicas, execute, DbRegister
from clickhouse_migrate.models.migration import MigrationMeta, Step


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
                ENGINE = MergeTree order by tuple(applyed_at);
            """
        )

    @classmethod
    def apply_migration(cls, step: Step, migration_meta: MigrationMeta):
        """
        Apply migration for several replicas or for only one db
        :param step: Migration step declared in migration file
        :param migration_meta: Meta that has to be written to the migrate table
        """
        if step.replicated:
            execute_for_replicas(query=step.sql)
        else:
            execute(query=step.sql)
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
            MigrationMeta(
                migration_id=record[0], migration_hash=record[1], filename=record[2]
            )
            for record in execute(query=query)
        ]
