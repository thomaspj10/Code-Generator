from __future__ import annotations
from abc import ABC, abstractmethod
from language import Language

class CodeBuilder(ABC):

    # Additional builders who are required for this builder to work.
    _required_builders: list[CodeBuilder]

    def __init__(self) -> None:
        super().__init__()
        self._required_builders = []

    def _add_required_builder(self, builder: CodeBuilder):
        self._required_builders.append(builder)

    @abstractmethod
    def build(self, language: Language) -> str:
        pass
