class ConfigError(Exception):
    MESSAGE = "Wrong parameters were provided"

    def __init__(self, message: str = MESSAGE):
        super().__init__(message)
