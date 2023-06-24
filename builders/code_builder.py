from abc import ABC, abstractmethod
from language import Language

class CodeBuilder(ABC):

    @abstractmethod
    def build(self, language: Language) -> str:
        pass
