from abc import ABC, abstractmethod


class AbstractDatabase(ABC):
    @abstractmethod
    def insert_poll(self, poll):
        pass

    @abstractmethod
    def get_poll(self):
        pass
