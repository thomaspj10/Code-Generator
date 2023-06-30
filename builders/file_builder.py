from builders.code_builder import CodeBuilder
from string_builder import StringBuilder
from language import Language
from typing import Self
import os.path

class FileBuilder:

    __builders: list[CodeBuilder]

    def __init__(self) -> None:
        self.__builders = []

    def add(self, builder: CodeBuilder) -> Self:
        self.__builders.append(builder)

        for required_builder in builder._required_builders: # type: ignore
            if required_builder not in self.__builders:
                self.__builders.append(required_builder)

        return self

    def build(self, language: Language, module_name: str) -> str:
        sb = StringBuilder()

        if language == Language.PYTHON:
            sb.add_line("from __future__ import annotations")
            sb.add_line("from dataclasses import dataclass")
            sb.empty_line()
            sb.empty_line()

        if language == Language.ELM:
            sb.add_line(f"module {module_name} exposing (..)")
            sb.empty_line()
            sb.empty_line()

        return sb.build() + "\n".join([builder.build(language) for builder in self.__builders]) + "\n"
    
    def save(self, file_name: str, directory: str, language: Language):
        module_name = file_name.split(".")[0]
        with open(os.path.join(directory, file_name), "w") as f:
            f.write(self.build(language, module_name))

def file_builder():
    return FileBuilder()
