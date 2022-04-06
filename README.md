# ClickHouse Migrate
[![codecov](https://codecov.io/gh/trushad0w/clickhouse-migrate/branch/master/graph/badge.svg?token=WSTIR7MOHG)](https://codecov.io/gh/trushad0w/clickhouse-migrate)
[![PyPI version](https://badge.fury.io/py/clickhouse-migrate.svg)](https://badge.fury.io/py/clickhouse-migrate)


Python library for applying migrations in ClickHouse database.

## Installation

Installation via PyPi:
```shell
pip install clickhouse-migrate
```

## Configuration

### .ini file
To configure and use `clickhouse-migrate` we can create a `*.ini` configuration file with the following content

```ini
[databases]
# Here we should provide a connection string to a database
# In case of using a replicated ClickHouse instance one should provide all connection strings
# related to this particular replicated instance
connection_strings = [
        "clickhouse+native://default:@localhost:9000/clickhouse_migrate"
    ]

[migration_path]
# Here we should provide a path to the selected migration folder
directory = "./migrations"

```

Default name that is used by `clickhouse-migrate` library is `clickhouse_migrate.ini`
Configurator will search for this file by default.

### Environment variables
Another configuration option is to use environment variables
```shell

CLICKHOUSE_MIGRATE_DATABASES='["<connection_string_1>", ... ,"<connection_string_n>"]'
CLICKHOUSE_MIGRATE_DIRECTORY=<path to directory with migrations files>

```

### Command line arguments
If the above mentioned methods is also not applicable for the project, one can use command line arguments
`-db` / `--databases` —  Databases list
`-dir` / `--migration_dir` — Migrations directory

## Usage

### Create migration file

One can create a new migration via calling `clickhouse-migrate create_migration` command.

#### Command parameters:

`-n` / `--name <name of a new migration file>` — this is a required parameter 

`-c` / `--config <path to the created config file>` — this is an optional parameter, 
one may want to use it when the config file is not located in the root directory 
or if its' name is different from default one

`-db` / `--databases` — optional parameter for providing database connection strings

`-dir` / `--migration_dir` — optional parameter for providing path to directory with migration files

Example usage:
```shell
clickhouse-migrate create_migration -n test_migration -c /home/clickhouse-migrate/config/conf.ini
```

```shell
clickhouse-migrate create_migration -n test_migration -dir /home/my_project/migrations -db clickhouse+native://default:@localhost:9000/db -db clickhouse+native://default:@localhost:9001/db
```

After calling the above-mentioned command a blank migration file `YYYY-MM-DD-HH-mm-ss_<migration_name>.py`
will be created in the directory which was defined in the `*.ini` configuration file.

The content of the created file will look like this
```python
from clickhouse_migrate import Step

migrations = [Step(sql="")]
```
One should use `Step` dataclass to create migrations. Migrations would be applied in the same order that they are stated in the `migrations` list variable.
All of listed changes in the `migration` list variable are by default applied to all databases listed in the `*.ini` config file, since usually changes are required for all replicated instances.

If an SQL query stated in the `Step` dataclass should not be executed for all DB replicas one may use `Step(sql="<sql query>", replicated=False)` statement.

This rule does not apply in case there is only one connection string in `*.ini` file.

### Apply migrations

One can apply migrations created via `clickhouse-migrate create_migration` command by calling `clickhouse-migrate migrate`.

#### Command parameters:
`--config <path to the created config file>` — this is an optional parameter, 
one may want to use it when the config file is not located in the root directory 
or if its' name is different from default one

`-db` / `--databases` — optional parameter for providing database connection strings

`-dir` / `--migration_dir` — optional parameter for providing path to directory with migration files

Example usage:
```shell
clickhouse-migrate migrate -c /home/clickhouse-migrate/config/conf.ini
```

```shell
clickhouse-migrate migrate -dir /home/my_project/migrations -db clickhouse+native://default:@localhost:9000/db
```

After calling this command all changes from migration files will be applied step-by-step. Changes are stored in `clickhouse_migrate` table.
