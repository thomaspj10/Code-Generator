from __future__ import annotations

from builders.code_builder import CodeBuilder

from dataclasses import dataclass
from typing import Self
from string_builder import StringBuilder
from language import Language
from type import Type, get_type

@dataclass
class Attribute:
    name: str
    type: Type | ClassBuilder
    generic_arguments: list[Type | ClassBuilder]

class ClassBuilder(CodeBuilder):
    
    __name: str
    __attributes: list[Attribute]

    def __init__(self, name: str) -> None:
        super().__init__()
        self.__name = name
        self.__attributes = []
    
    def attribute(self, name: str, type: Type, generic_arguments: list[Type | ClassBuilder] | None = None) -> Self:
        if generic_arguments != None:
            for argument in generic_arguments:
                if isinstance(argument, ClassBuilder):
                    self._add_required_builder(argument)

        self.__attributes.append(Attribute(name, type, [] if generic_arguments == None else generic_arguments))
        return self
    
    def _get_type(self, language: Language, attribute: Attribute) -> str:
        if isinstance(attribute.type, ClassBuilder):
            return attribute.type.__name
        
        generic_arguments: list[str] = []
        for item in attribute.generic_arguments:
            if isinstance(item, Type):
                generic_arguments.append(get_type(language, item, []))
            else:
                generic_arguments.append(item.__name)

        return get_type(language, attribute.type, generic_arguments) 
    
    def build(self, language: Language) -> str:
        sb = StringBuilder()

        if language == Language.PYTHON:
            sb.add_line("@dataclass")
            sb.add_line(f"class {self.__name}:")
            for attribute in self.__attributes:
                sb.add_line(f"{attribute.name}: {self._get_type(language, attribute)}", indent=1)

        if language == Language.ELM:
            sb.add_line(f"type alias {self.__name} =")

            for index, attribute in enumerate(self.__attributes):
                start = "{ " if index == 0 else ", "
                sb.add_line(f"{start}{attribute.name} : {self._get_type(language, attribute)}", indent=1)

            sb.add_line("}", indent=1)

        return sb.build()

def class_builder(name: str):
    return ClassBuilder(name)
