from enum import Enum
from language import Language

class Type(Enum):
    STRING = "string"
    INT = "int"
    FLOAT = "float"

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
}

def get_type(language: Language, type: Type):
    return TYPE_MAPPING[type][language]
