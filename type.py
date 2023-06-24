from enum import Enum
from language import Language

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
