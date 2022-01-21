class ConfigError(Exception):
    MESSAGE = "Wrong parameters inside config ini file"

    def __init__(self, message: str = MESSAGE):
        super().__init__(message)
