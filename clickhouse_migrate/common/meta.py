class Singleton(type):
    """
    Metaclass which implements singleton logic
    """

    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.__instances[cls]

    def drop_object(cls):
        if cls in cls.__instances:
            object_to_drop = cls.__instances.pop(cls)
            del object_to_drop
