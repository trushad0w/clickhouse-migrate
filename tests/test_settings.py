from os import environ

from clickhouse_migrate.conf.settings import Settings


def test_init_config_env(reset_env):
    conn_str = "conn_str"
    migrations = "migrations"
    cluster_name = "cluster"
    is_in_cluster = "True"

    environ[Settings.CH_CONN_STR_VARIABLE] = conn_str
    environ[Settings.DIRECTORY_ENV_VAR] = migrations
    environ[Settings.CLUSTER_NAME] = cluster_name
    environ[Settings.IS_IN_CLUSTER] = is_in_cluster

    Settings().init_config()

    assert Settings().conn_str == conn_str, "Clickhouse connection string value should be taken from env"
    assert Settings().migration_dir == migrations, "Migrations value should be taken from env"
    assert Settings().cluster_name == cluster_name, "Cluster name value should be taken from env"
    assert Settings().is_in_cluster == is_in_cluster, "Is in cluster value should be taken from env"


def test_init_config_args(reset_env):
    conn_str = "conn_str"
    migrations = "migrations"
    cluster_name = "cluster"
    is_in_cluster = True

    environ[Settings.CH_CONN_STR_VARIABLE] = "env_conn_str"
    environ[Settings.DIRECTORY_ENV_VAR] = "env_migrations"
    environ[Settings.CLUSTER_NAME] = "env_cluster"
    environ[Settings.IS_IN_CLUSTER] = "env_migrations"

    Settings().init_config(
        migration_dir=migrations, conn_str=conn_str, is_in_cluster=is_in_cluster, cluster_name=cluster_name
    )

    assert Settings().conn_str == conn_str, "Clickhouse connection string value should be taken from args"
    assert Settings().migration_dir == migrations, "Migrations value should be taken from args"
    assert Settings().cluster_name == cluster_name, "Cluster name value should be taken from args"
    assert Settings().is_in_cluster == is_in_cluster, "Is in cluster value should be taken from args"
