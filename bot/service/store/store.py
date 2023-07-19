from abc import ABC, abstractmethod

class Store_interaction(ABC):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @abstractmethod
    def extract(self) -> list:
        pass

    @abstractmethod
    def put(self, data, position):
        pass

    @abstractmethod
    def get_free_slots(self) -> dict:
        pass
