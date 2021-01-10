class GardenMeta(type):
    _instances = {}
    def __call__(mcs, cls, *args, **kwargs):
        if cls not in mcs._instances:
            [cls]