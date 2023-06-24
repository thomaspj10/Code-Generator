from builders.code_builder import CodeBuilder

from dataclasses import dataclass
from typing import Self
from string_builder import StringBuilder
from language import Language
from type import Type, get_type

@dataclass
class Attribute:
    name: str
    type: Type

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
        sb = StringBuilder()

        if language == Language.PYTHON:
            sb.add_line(f"class {self.__name}:")
            for attribute in self.__attributes:
                sb.add_line(f"{attribute.name}: {get_type(language, attribute.type)}", indent=1)

        if language == Language.ELM:
            sb.add_line(f"type alias {self.__name} =")

            for index, attribute in enumerate(self.__attributes):
                start = "{ " if index == 0 else ", "
                sb.add_line(f"{start}{attribute.name} : {get_type(language, attribute.type)}", indent=1)

            sb.add_line("}", indent=1)

        return sb.build()

def class_builder():
    return ClassBuilder()
