from os import environ

from clickhouse_migrate.conf.settings import Settings


def test_init_config_env(reset_env):
    databases = "databases"
    migrations = "migrations"

    environ[Settings.DATABASES_ENV_VAR] = databases
    environ[Settings.DIRECTORY_ENV_VAR] = migrations

    Settings().init_config()

    assert Settings().databases == [databases], "Databases value should be taken from env"
    assert Settings().migration_dir == migrations, "Migrations value should be taken from env"


def test_init_config_args(reset_env):
    databases = ["databases"]
    migrations = "migrations"

    environ[Settings.DATABASES_ENV_VAR] = "env_databases"
    environ[Settings.DIRECTORY_ENV_VAR] = "env_migrations"

    Settings().init_config(databases=databases, migration_dir=migrations)

    assert Settings().databases == databases, "Databases value should be taken from arguments"
    assert Settings().migration_dir == migrations, "Migrations value should be taken from arguments"
