import configparser
import json
from os import path

from clickhouse_migrate.common.exceptions.config import ConfigError
from clickhouse_migrate.common.meta import Singleton

CURRENT_DIR = path.abspath(path.dirname(__file__))
CONFIG_PATH = path.join(CURRENT_DIR, "clickhouse_migrate.ini")


class Settings(metaclass=Singleton):
    databases = None
    migration_dir = None

    def init_config(self, config_path: str):
        try:
            config = configparser.ConfigParser()
            config.read(config_path)

            self.databases = json.loads(config.get("databases", "connection_strings"))
            self.migration_dir = json.loads(config.get("migration_path", "directory"))

        except KeyError:
            raise ConfigError("Variables: connection_strings, directory must be provided in the *.ini config file")
