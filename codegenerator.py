from __future__ import annotations
from dataclasses import dataclass
from language import Language, format_class_name
from type import Type, get_type

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
    
    result += "from annotations import __future__\n"
    result += "from dataclasses import dataclass\n"

    for dto in dtos:
        result += "\n@dataclass\n"
        result += f"class {dto.name}\n"
        for attribute in dto.attributes:
            result += f"{INDENT}{attribute.name}: {type_to_code(attribute.type, Language.PYTHON)}\n"
        

    return result

def generate_elm(dtos: list[CustomDto]) -> str:
    INDENT = " " * 4
    result = ""

    result += "import Json.Decode as JD\n"
    result += "import Json.Encode as JE\n"
    result += "import Json.Decode.Pipeline as JDP\n"

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
            result += f"{INDENT * 2}|> JDP.required \"{attribute.name}\" {type_to_code(attribute.type, Language.ELM_DECODERS)}\n"

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
            result += f"{INDENT * 2}{char} ( \"{attribute.name}\", {type_to_code(attribute.type, Language.ELM_ENCODERS)} object.{attribute.name} )\n"
        result += INDENT * 2 + "]\n"

    return result

def store_python(file: str):
    with open(file, "w") as f:
        f.write(generate_python(DTOS))

def store_elm(file: str):
    with open(file, "w") as f:
        f.write(generate_elm(DTOS))
