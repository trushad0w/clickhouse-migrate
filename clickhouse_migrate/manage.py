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
@click.option("-db", "--databases", help="Databases list", required=False, multiple=True)
@click.option(
    "-dir",
    "--migration_dir",
    help="Migrations directory",
    required=False,
    type=click.Path(exists=True),
)
def migrate(databases: List[str], migration_dir: str):
    Settings().init_config(migration_dir=migration_dir, databases=databases)
    check_migrations_dir()
    check_databases()
    DbRegister().setup_db()

    MigrationService.apply_initial_step()
    MigrationService().apply_all_migrations()

    dispose()


@click.command(name="create_migration")
@click.option("-n", "--name", help="migration name", required=True)
@click.option(
    "-dir",
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
