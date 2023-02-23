from typing import List

import click

from clickhouse_migrate.common.db import DbRegister
from clickhouse_migrate.conf.settings import Settings
from clickhouse_migrate.interfaces.service import MigrationService
from clickhouse_migrate.validation import check_databases, check_migrations_dir


@click.group()
def cli():
    pass


@click.command(name="migrate")
@click.option(
    "--conn_str", help="Clickhouse connection string clickhouse+native://db@host:port/database", required=False
)
@click.option(
    "--migration_dir",
    help="Migrations directory",
    required=False,
    type=click.Path(exists=True),
)
@click.option(
    "--is_in_cluster",
    help="Migrations directory",
    required=False,
    type=bool,
)
@click.option("--cluster_name", help="Name of Clickhouse cluster", required=False)
def migrate(conn_str: str, migration_dir: str, is_in_cluster: bool, cluster_name: str):
    Settings().init_config(
        migration_dir=migration_dir, conn_str=conn_str, is_in_cluster=is_in_cluster, cluster_name=cluster_name
    )
    check_migrations_dir()
    check_databases()
    DbRegister().setup_db()

    MigrationService.apply_initial_step()
    MigrationService().apply_all_migrations()

    dispose()


@click.command(name="create_migration")
@click.option("--name", help="migration name", required=True)
@click.option(
    "--migration_dir",
    help="Migrations directory",
    required=False,
    type=click.Path(exists=True),
)
def create_migration(name: str, migration_dir: str):
    Settings().init_config(migration_dir=migration_dir)
    check_migrations_dir()

    MigrationService.create_new_migration(name)
    dispose()


def dispose():
    Settings.dispose()
    DbRegister.dispose()


cli.add_command(migrate)
cli.add_command(create_migration)


def main():
    cli()


if __name__ == "__main__":
    cli()
