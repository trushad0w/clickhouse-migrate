import os
from os import path
from urllib.parse import urlparse

from click.testing import CliRunner
from clickhouse_driver import connect
from pytest import fixture
from pytest_mock import MockFixture

from clickhouse_migrate.common.db import DbRegister
from clickhouse_migrate.conf.settings import Settings

CURRENT_DIR = path.abspath(path.dirname(__file__))
CONFIG_PATH = path.join(CURRENT_DIR, "clickhouse_migrate.ini")

MIGRATION_FILE = "2022-01-19-14-25-17_init_migration.py"
MIGRATION_PATH = path.join(CURRENT_DIR, f"migrations/{MIGRATION_FILE}")
MIGRATION_CONTENT = """
from clickhouse_migrate import Step

migrations = [Step(sql="select * from clickhouse_migrate"), Step(sql="select 1 from clickhouse_migrate")]
"""


@fixture
def runner():
    return CliRunner()


@fixture(autouse=True, scope="session")
def setup_for_tests(session_mocker: MockFixture):
    Settings().init_config(config_path=CONFIG_PATH)
    db_url = urlparse(Settings().databases[0])
    db_name = db_url.path.replace("/", "")
    db_host = f"{db_url.scheme}://{db_url.netloc}"
    connection = connect(db_host)
    connection.cursor().execute(f"create database if not exists {db_name}")
    DbRegister().setup_db()

    yield
    connection.cursor().execute(f"drop database if exists {db_name}")


@fixture(autouse=True, scope="session")
def create_test_migration():
    with open(MIGRATION_PATH, "w") as migration_file:
        migration_file.write(MIGRATION_CONTENT)
    yield
    delete_test_migration()


def create_changed_migration():
    content = MIGRATION_CONTENT.replace("select *", "select 1")
    with open(MIGRATION_PATH, "w") as migration_file:
        migration_file.write(content)


def delete_test_migration():
    os.remove(MIGRATION_PATH)
