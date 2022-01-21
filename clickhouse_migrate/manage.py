import click

from clickhouse_migrate.common.db import DbRegister
from clickhouse_migrate.conf.settings import Settings, CONFIG_PATH
from clickhouse_migrate.interfaces.service import MigrationService


@click.group()
def cli():
    pass


@click.command(name="migrate")
@click.option("--config", help="Path to config *.ini file", default=CONFIG_PATH)
def migrate(config: str):
    Settings().init_config(config_path=config)
    DbRegister().setup_db()
    MigrationService.apply_initial_step()
    MigrationService().apply_all_migrations()


@click.command(name="create_migration")
@click.option("--name", help="migration name", required=True)
@click.option("--config", help="Path to config *.ini file", default=CONFIG_PATH)
def create_migration(name: str, config: str):
    Settings().init_config(config_path=config)
    MigrationService.create_new_migration(name)


cli.add_command(migrate)
cli.add_command(create_migration)


def main():
    cli()


if __name__ == "__main__":
    cli()
