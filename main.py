from typing import Self, Any
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass

INDENT = "    "

class Language(Enum):
    PYTHON = "python"
    ELM = "elm"

@dataclass
class Attribute:
    name: str
    type: str
    default_value: Any | None

class CodeBuilder(ABC):

    @abstractmethod
    def build(self, language: Language) -> str:
        pass

class ClassBuilder(CodeBuilder):
    
    __name: str
    __attributes: list[Attribute]

    def __init__(self) -> None:
        self.__name = ""
        self.__attributes = []

    def name(self, name: str) -> Self:
        self.__name = name
        return self
    
    def attribute(self, name: str, type: str, default_value: Any | None = None) -> Self:
        self.__attributes.append(Attribute(name, type, default_value))
        return self
    
    def build(self, language: Language) -> str:
        result = ""

        if language == Language.PYTHON:
            result += f"class {self.__name}:\n"
            for attribute in self.__attributes:
                default_value_result = "" if attribute.default_value == None else f" = {attribute.default_value}"
                result += f"{INDENT}{attribute.name}: {attribute.type}{default_value_result}\n"

        if language == Language.ELM:
            result += f"type alias {self.__name} = " + "{\n"

            for attribute in self.__attributes:
                result += f"{INDENT}{attribute.name} : {attribute.type},\n"

            result += "}"

        return result

def class_builder():
    return ClassBuilder()

cls = (
    class_builder()
    .name("Person")
    .attribute("name", "str")
    .build(Language.ELM)
)

print(cls)
