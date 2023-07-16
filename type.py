from enum import Enum
from language import Language

class Type(Enum):
    STRING = "string"
    INT = "int"
    FLOAT = "float"
    CLASS = "class"
    LIST = "list"

TYPE_MAPPING: dict[Type, dict[Language, str]] = {
    Type.STRING: {
        Language.PYTHON: "str",
        Language.ELM: "String"
    },
    Type.INT: {
        Language.PYTHON: "int",
        Language.ELM: "Int"
    },
    Type.FLOAT: {
        Language.PYTHON: "float",
        Language.ELM: "Float"
    },
    Type.CLASS: {
        Language.PYTHON: "{0}",
        Language.ELM: "{0}"
    },
    Type.LIST: {
        Language.PYTHON: "list[{0}]",
        Language.ELM: "List {0}"
    },
}

def get_type(language: Language, type: Type, generic_arguments: list[str]):
    return TYPE_MAPPING[type][language].format(*generic_arguments)
