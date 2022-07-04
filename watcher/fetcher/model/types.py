from enum import Enum

class FuelStationState(Enum):
    UNKNOWN = 0
    OPEN = 1
    LIMITED = 2
    CLOSED = 3

    def __str__(self):
        return f'{self.name}'

class Fuel:
    class Gasoline(Enum):
        A95 = 1
        A95E = 2
        A98 = 3
        A98E = 4
        A100 = 5
        A100E = 6
        A92 = 7

        def __str__(self):
            return f'{self.name}'

    class Diesel(Enum):
        DP = 1
        DPE = 2

        def __str__(self):
            return f'{self.name}'

    class Other(Enum):
        UNKNOWN = 1
        IRRELEVANT = 2 
        LPG = 3

        def __str__(self):
            return f'{self.name}'

    class Status(Enum):
        UNKNOWN = 0
        AVALIABLE = 1
        LIMITED = 2
        SPECONLY = 3
        MISSING = 4

        def __str__(self):
            return f'{self.name}'

class FuelStation:
    TEMPLATE = {
        'ID': None,
        'LINK': None, 
        'CITY': None, 
        'ADDRESS': None,
        'STATUS': None,
        'DATE': None,
        'LOCATION': None,
        'PROVIDER': None
    }

    def getTemplate():
        return FuelStation.TEMPLATE.copy()

    def default():
        return FuelStation(**FuelStation.TEMPLATE)

    def copy(self):
        return FuelStation(**self.__dict__)

    def __init__(self, **kwargs):
        self.update(**FuelStation.TEMPLATE)
        self.update(**kwargs)

    def __str__(self):
        return str(self.__dict__)

    def update(self, **kwargs):
        self.__dict__.update(kwargs)

    def set(self, k, v):
        self.update(**{k:v})

    def drop(self, k):
        del self.__dict__[k]