import click

from clickhouse_migrate.common.db import DbRegister
from clickhouse_migrate.conf.settings import Settings
from clickhouse_migrate.interfaces.service import MigrationService


@click.group()
def cli():
    pass


@click.command(name="migrate")
@click.option("-c", "--config", help="Path to config *.ini file", required=False)
@click.option(
    "-db", "--databases", help="Databases list", required=False, multiple=True
)
@click.option(
    "-dir",
    "--migration_dir",
    help="Migrations directory",
    required=False,
    type=click.Path(exists=True),
)
def migrate(config: str, databases: str, migration_dir: str):
    Settings().init_config(
        config_path=config, databases=databases, migration_dir=migration_dir
    )
    DbRegister().setup_db()
    MigrationService.apply_initial_step()
    MigrationService().apply_all_migrations()


@click.command(name="create_migration")
@click.option("-n", "--name", help="migration name", required=True)
@click.option("-c", "--config", help="Path to config *.ini file", required=False)
@click.option(
    "-db", "--databases", help="Databases list", required=False, multiple=True
)
@click.option(
    "-dir",
    "--migration_dir",
    help="Migrations directory",
    required=False,
    type=click.Path(exists=True),
)
def create_migration(name: str, config: str, databases: str, migration_dir: str):
    Settings().init_config(
        config_path=config, databases=databases, migration_dir=migration_dir
    )
    MigrationService.create_new_migration(name)


cli.add_command(migrate)
cli.add_command(create_migration)


def main():
    cli()


if __name__ == "__main__":
    cli()
