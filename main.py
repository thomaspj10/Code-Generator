from __future__ import annotations
from typing import Self
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass

INDENT = "    "

class Language(Enum):
    PYTHON = "python"
    ELM = "elm"

TYPE_MAPPING = {
    "string": {
        "python": "str",
        "elm": "String"
    },
    "int": {
        "python": "int",
        "elm": "Int"
    },
    "float": {
        "python": "float",
        "elm": "Float"
    },
}

class Type(Enum):
    STRING = "string"
    INT = "int"
    FLOAT = "float"

def get_type(language: Language, type: Type):
    return TYPE_MAPPING[type.value][language.value]

@dataclass
class Attribute:
    name: str
    type: Type

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
    
    def attribute(self, name: str, type: Type) -> Self:
        self.__attributes.append(Attribute(name, type))
        return self
    
    def build(self, language: Language) -> str:
        result = ""

        if language == Language.PYTHON:
            result += f"class {self.__name}:\n"
            for attribute in self.__attributes:
                result += f"{INDENT}{attribute.name}: {get_type(language, attribute.type)}\n"

        if language == Language.ELM:
            result += f"type alias {self.__name} = " + "{\n"

            for attribute in self.__attributes:
                result += f"{INDENT}{attribute.name} : {get_type(language, attribute.type)},\n"

            result += "}"

        return result

def class_builder():
    return ClassBuilder()

cls = (
    class_builder()
    .name("Person")
    .attribute("name", Type.STRING)
    .build(Language.ELM)
)

print(cls)
