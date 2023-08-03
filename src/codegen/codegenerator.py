from __future__ import annotations
from dataclasses import dataclass
from codegen.language import Language, format_class_name

from enum import Enum

class Type(Enum):
    INT = "int"
    STRING = "string"
    BOOLEAN = "boolean"
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
    Type.BOOLEAN: {
        Language.PYTHON: "bool",
        Language.ELM: "Bool",
        Language.ELM_DECODERS: "JD.bool",
        Language.ELM_ENCODERS: "JE.bool",
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
        Language.ELM_ENCODERS: "encodeNullable {0}",
    },
}

def get_type(language: Language, type: Type, generic_arguments: list[str]):
    return TYPE_MAPPING[type][language].format(*generic_arguments)


DTOS: list[CustomDto] = []

class CustomType:
    
    type: CustomType | Type | str
    generic_arguments: list[CustomType]

    def __init__(self, type: CustomType | Type | str, generic_arguments: list[CustomType]) -> None:
        self.type = type
        self.generic_arguments = generic_arguments

def list_(type: CustomType | Type):
    return CustomType(Type.LIST, [CustomType(type, [])])

def cls(dto: CustomDto):
    return CustomType(Type.CLASS, [CustomType(dto.name, [])])

def maybe(type: CustomType | Type):
    return CustomType(Type.MAYBE, [CustomType(type, [])])

def dto(name: str) -> CustomDto:
    return CustomDto(name)

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
        DTOS.append(self)

    def attribute(self, name: str, type: CustomType | Type):
        if isinstance(type, Type):
            type = CustomType(type, [])

        self.attributes.append(Attribute(name, type))

        return self

def type_to_code(custom_type: CustomType, language: Language) -> str:
    if isinstance(custom_type.type, str):
        return format_class_name(custom_type.type, language)

    if isinstance(custom_type.type, Type):
        return get_type(language, custom_type.type, [type_to_code(argument, language) for argument in custom_type.generic_arguments])

    return type_to_code(custom_type.type, language)

def generate_python(dtos: list[CustomDto]) -> str:
    INDENT = " " * 4
    result = ""
    
    result += "from __future__ import annotations\n"
    result += "from dataclasses import dataclass\n"

    for dto in dtos:
        result += "\n@dataclass\n"
        result += f"class {dto.name}:\n"
        for attribute in dto.attributes:
            result += f"{INDENT}{attribute.name}: {type_to_code(attribute.type, Language.PYTHON)}\n"
        

    return result

def generate_elm(dtos: list[CustomDto]) -> str:
    INDENT = " " * 4
    result = ""

    result += "module Types exposing (..)\n\n"

    result += "import Json.Decode as JD\n"
    result += "import Json.Encode as JE\n"
    result += "import Json.Decode.Pipeline as JDP\n"

    result += """
encodeNullable : (value -> JE.Value) -> Maybe value -> JE.Value
encodeNullable valueEncoder maybeValue =
    case maybeValue of
        Just value ->
            valueEncoder value

        Nothing ->
            JE.null
"""

    # Generate the models
    for dto in dtos:
        result += f"\ntype alias {dto.name} =\n"

        for index, attribute in enumerate(dto.attributes):
            char = "{" if index == 0 else ","
            result += f"{INDENT}{char} {attribute.name} : {type_to_code(attribute.type, Language.ELM)}\n"
        
        result += INDENT + "}\n"

    result += generate_elm_decoders(dtos)
    result += generate_elm_encoders(dtos)

    return result


def generate_elm_decoders(dtos: list[CustomDto]) -> str:
    INDENT = " " * 4
    result = ""
    
    for dto in dtos:
        decoder_name = format_class_name(dto.name, Language.ELM_DECODERS)

        result += f"\n{decoder_name} : JD.Decoder {dto.name}\n"
        result += f"{decoder_name} =\n"
        result += f"{INDENT}JD.succeed {dto.name}\n"

        for attribute in dto.attributes:
            result += f"{INDENT * 2}|> JDP.required \"{attribute.name}\" ({type_to_code(attribute.type, Language.ELM_DECODERS)})\n"

    return result

def generate_elm_encoders(dtos: list[CustomDto]) -> str:
    INDENT = " " * 4
    result = ""
    
    for dto in dtos:
        encoder_name = format_class_name(dto.name, Language.ELM_ENCODERS)

        result += f"\n{encoder_name} : {dto.name} -> JE.Value\n"
        result += f"{encoder_name} object =\n"
        result += f"{INDENT}JE.object\n"

        for index, attribute in enumerate(dto.attributes):
            char = "[" if index == 0 else ","
            result += f"{INDENT * 2}{char} ( \"{attribute.name}\", ({type_to_code(attribute.type, Language.ELM_ENCODERS)} object.{attribute.name}) )\n"
        result += INDENT * 2 + "]\n"

    return result

def store_python(file: str):
    with open(file, "w") as f:
        f.write(generate_python(DTOS))

def store_elm(file: str):
    with open(file, "w") as f:
        f.write(generate_elm(DTOS))
