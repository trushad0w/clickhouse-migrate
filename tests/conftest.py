from os import environ, mkdir, path
from shutil import rmtree
from urllib.parse import urlparse

import pytest
from click.testing import CliRunner
from clickhouse_driver import connect

from clickhouse_migrate.common.db import DbRegister
from clickhouse_migrate.conf.settings import Settings

CURRENT_DIR = path.abspath(path.dirname(__file__))

MIGRATION_FILE = "2022-01-19-14-25-17_init_migration.py"
MIGRATION_DIR = path.join(CURRENT_DIR, "migrations")
MIGRATION_FILE_PATH = path.join(MIGRATION_DIR, f"{MIGRATION_FILE}")
MIGRATION_CONTENT = """
from clickhouse_migrate import Step

migrations = [Step(sql="select * from clickhouse_migrate"), Step(sql="select 1 from clickhouse_migrate")]
"""


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def setup_for_tests():
    Settings().init_config()
    if Settings().databases:
        db_url = urlparse(Settings().databases[0])
        db_name = db_url.path.replace("/", "")
        db_host = f"{db_url.scheme}://{db_url.netloc}"
        connection = connect(db_host)
        connection.cursor().execute(f"create database if not exists {db_name}")
        DbRegister().setup_db()
        yield
        connection.cursor().execute(f"drop database if exists {db_name}")
    else:
        yield

    Settings.dispose()
    DbRegister.dispose()


@pytest.fixture(autouse=True)
def create_test_migration():
    mkdir(MIGRATION_DIR)
    with open(MIGRATION_FILE_PATH, "w") as migration_file:
        migration_file.write(MIGRATION_CONTENT)
    yield
    rmtree(MIGRATION_DIR)


def create_changed_migration():
    rmtree(MIGRATION_DIR)
    content = MIGRATION_CONTENT.replace("select *", "select 1")
    mkdir(MIGRATION_DIR)
    with open(MIGRATION_FILE_PATH, "w") as migration_file:
        migration_file.write(content)


@pytest.fixture()
def reset_env():
    databases = environ.get(Settings.DATABASES_ENV_VAR)
    migration_dir = environ.get(Settings.DIRECTORY_ENV_VAR)

    yield

    if databases:
        environ[Settings.DATABASES_ENV_VAR] = databases
    else:
        environ.pop(Settings.DATABASES_ENV_VAR)

    if migration_dir:
        environ[Settings.DIRECTORY_ENV_VAR] = migration_dir
    else:
        environ.pop(Settings.DIRECTORY_ENV_VAR)
