from typing import List

from clickhouse_migrate.common.db import execute
from clickhouse_migrate.models.migration import MigrationMeta
from conf.settings import Settings


class MigrationRepo:
    @classmethod
    def init_migration_table(cls) -> None:
        """
        Migration initialization, creates table to track the history of applied migrations
        :return: None
        """
        if Settings().is_in_cluster:
            cls.init_migration_table_on_cluster()
        else:
            cls.init_migration_table_single_node()

    @staticmethod
    def init_migration_table_single_node() -> None:
        """
        Method for migration initialization
        It creates table to store info about applied migrations in a single node clickhouse instance
        :return: None
        """
        execute(
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

    @staticmethod
    def init_migration_table_on_cluster() -> None:
        """
        Method for migration initialization
        It creates table to store info about applied migrations in a clustered clickhouse instance
        :return: None
        """
        execute(
            """
                create table if not exists clickhouse_migrate on cluster %(cluster_name)s (
                        migration_id String,
                        migration_hash String,
                        filename String,
                        applyed_at DateTime default now()
                    )
                engine = ReplicatedMergeTree('/clickhouse/tables/{shard}/{database}/clickhouse_migrate', '{replica}')
                order by tuple(applyed_at); 
            """,
            params={"cluster_name": Settings().cluster_name},
        )

    @classmethod
    def apply_migration(cls, sql: str, migration_meta: MigrationMeta) -> None:
        """
        Apply migration for several replicas or for only one db
        :param sql: Migration step sql that should be applied
        on each of the provided database instances or not
        :param migration_meta: Meta that has to be written to the migrate table
        """
        execute(query=sql)
        cls.insert_applied_migration_version(migration_meta=migration_meta)

    @staticmethod
    def insert_applied_migration_version(migration_meta: MigrationMeta):
        query = """
            insert into clickhouse_migrate (migration_id, migration_hash, filename)
            values (%(migration_id)s, %(migration_hash)s, %(filename)s)
        """
        execute(query=query, params=migration_meta.asdict())

    @staticmethod
    def get_applied_migrations() -> List[MigrationMeta]:
        query = """
            select migration_id, migration_hash, filename from clickhouse_migrate
        """
        return [
            MigrationMeta(migration_id=record[0], migration_hash=record[1], filename=record[2])
            for record in execute(query=query)
        ]
