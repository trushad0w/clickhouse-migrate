import glob
from pathlib import Path

import pytest

from clickhouse_migrate.common.db import execute
from clickhouse_migrate.conf.settings import Settings
from clickhouse_migrate.interfaces.service import MigrationService
from clickhouse_migrate.manage import create_migration, migrate
from tests.conftest import MIGRATION_DIR, create_changed_migration


def test_create_migration(runner):
    filename = "test_migration"
    result = runner.invoke(create_migration, ["--name", filename, "-dir", MIGRATION_DIR])
    assert result.exit_code == 0, f"Create migration command exited unsuccessfully: {result.exc_info}"
    file_list = [file for file in glob.glob(f"{MIGRATION_DIR}/*{filename}*.py")]
    assert len(file_list) > 0, "No migrations were found"

    path = Path(file_list[0])
    assert filename in path.stem, "Created file was not found"


def test_apply_initial_step():
    MigrationService.apply_initial_step()
    query = "select * from clickhouse_migrate"
    result = execute(query=query)
    assert result == [], "There should be no data in the table on migration table init"


def test_apply_migrations(runner):
    expected_result = set([f"2022-01-19-14-25-17_init_migration_{idx}" for idx in range(2)])
    result = runner.invoke(migrate, ["-dir", MIGRATION_DIR])
    assert result.exit_code == 0, f"Command exited unsuccessfully: {result.exc_info}"
    query = "select * from clickhouse_migrate"
    result = execute(query=query)
    assert (
        set([item[0] for item in result]) == expected_result
    ), "Expected migration result do not match with the received one"
    MigrationService().apply_all_migrations()
    assert (
        set([item[0] for item in result]) == expected_result
    ), "After second execution of migration task the same migrations were applied"


def test_apply_changed_migration():
    Settings().init_config(migration_dir=MIGRATION_DIR)
    MigrationService.apply_initial_step()
    MigrationService().apply_all_migrations()
    create_changed_migration()
    with pytest.raises(ValueError, match="Migration content changed"):
        MigrationService().apply_all_migrations()


@pytest.mark.parametrize(
    "query, expected_result",
    (
        (
            """
            create table testng on  cluster  test_cluster  as (
               select * from test
            ) engine Log;
            """,
            True,
        ),
        ("select on, cluster from test", False),
    ),
)
def test_is_on_cluster(query: str, expected_result: bool):
    assert MigrationService.is_on_cluster(sql=query) == expected_result
