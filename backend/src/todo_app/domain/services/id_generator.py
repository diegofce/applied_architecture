from abc import ABC, abstractmethod


class IdGenerator(ABC):
    @abstractmethod
    def next_id(self) -> str:
        raise NotImplementedError
