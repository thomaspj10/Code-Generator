from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from language import Language

class Type(Enum):
    INT = "int"
    STRING = "string"
    LIST = "list"
    CLASS = "class"
    MAYBE = "maybe"

class CustomType:
    
    type: CustomType | Type | str
    generic_arguments: list[CustomType]

    def __init__(self, type: CustomType | Type | str, generic_arguments: list[CustomType]) -> None:
        self.type = type
        self.generic_arguments = generic_arguments

TYPE_MAPPING: dict[Type, dict[Language, str]] = {
    Type.STRING: {
        Language.PYTHON: "str",
        Language.ELM: "String",
        Language.ELM_DECODE: "JD.string",
    },
    Type.INT: {
        Language.PYTHON: "int",
        Language.ELM: "Int",
        Language.ELM_DECODE: "JD.int",
    },
    Type.CLASS: {
        Language.PYTHON: "{0}",
        Language.ELM: "{0}",
        Language.ELM_DECODE: "{0}Decoder",
    },
    Type.LIST: {
        Language.PYTHON: "list[{0}]",
        Language.ELM: "List ({0})",
        Language.ELM_DECODE: "JD.list ({0})",
    },
    Type.MAYBE: {
        Language.PYTHON: "{0} | None",
        Language.ELM: "Maybe ({0})",
        Language.ELM_DECODE: "JD.maybe ({0})",
    },
}

def list_(type: CustomType | Type):
    return CustomType(Type.LIST, [CustomType(type, [])])

def cls(dto: CustomDto):
    return CustomType(Type.CLASS, [CustomType(dto.name, [])])

def maybe(type: CustomType | Type):
    return CustomType(Type.MAYBE, [CustomType(type, [])])

@dataclass
class Attribute:
    name: str
    type: CustomType

class CustomDto:
    
    name: str
    attributes: list[Attribute]

    def __init__(self, name: str) -> None:
        self.name = name
        self.attributes = []

    def attribute(self, name: str, type: CustomType | Type):
        if isinstance(type, Type):
            type = CustomType(type, [])

        self.attributes.append(Attribute(name, type))

        return self

address = (
    CustomDto("Address")
    .attribute("id", Type.INT)
    .attribute("name", Type.STRING)
)

person = (
    CustomDto("Person")
    .attribute("id", Type.INT)
    .attribute("name", Type.STRING)
    .attribute("address", cls(address))
)

type = cls(address)
type2 = list_(maybe(cls(address)))

def get_type(language: Language, type: Type, generic_arguments: list[str]):
    return TYPE_MAPPING[type][language].format(*generic_arguments)

def type_to_code(custom_type: CustomType, language: Language) -> str:
    if isinstance(custom_type.type, str):
        return custom_type.type

    if isinstance(custom_type.type, Type):
        return get_type(language, custom_type.type, [type_to_code(argument, language) for argument in custom_type.generic_arguments])

    return type_to_code(custom_type.type, language)

print(type_to_code(type, Language.ELM_DECODE))
print(type_to_code(type2, Language.ELM_DECODE))
