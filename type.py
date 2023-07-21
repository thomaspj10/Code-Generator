from enum import Enum
from language import Language

class Type(Enum):
    INT = "int"
    STRING = "string"
    LIST = "list"
    CLASS = "class"
    MAYBE = "maybe"

TYPE_MAPPING: dict[Type, dict[Language, str]] = {
    Type.STRING: {
        Language.PYTHON: "str",
        Language.ELM: "String",
        Language.ELM_DECODERS: "JD.string",
        Language.ELM_ENCODERS: "JE.string",
    },
    Type.INT: {
        Language.PYTHON: "int",
        Language.ELM: "Int",
        Language.ELM_DECODERS: "JD.int",
        Language.ELM_ENCODERS: "JE.int",
    },
    Type.CLASS: {
        Language.PYTHON: "{0}",
        Language.ELM: "{0}",
        Language.ELM_DECODERS: "{0}",
        Language.ELM_ENCODERS: "{0}",
    },
    Type.LIST: {
        Language.PYTHON: "list[{0}]",
        Language.ELM: "List ({0})",
        Language.ELM_DECODERS: "JD.list ({0})",
        Language.ELM_ENCODERS: "JE.list ({0})",
    },
    Type.MAYBE: {
        Language.PYTHON: "{0} | None",
        Language.ELM: "Maybe ({0})",
        Language.ELM_DECODERS: "JD.maybe ({0})",
        Language.ELM_ENCODERS: "{0}",
    },
}

def get_type(language: Language, type: Type, generic_arguments: list[str]):
    return TYPE_MAPPING[type][language].format(*generic_arguments)
