class DatabaseError(Exception):
    pass


class UnknownInstanceError(DatabaseError):
    MESSAGE = "Unknown connection, provided pool name is not present in the register"

    def __init__(self, message: str = MESSAGE):
        super().__init__(message)
