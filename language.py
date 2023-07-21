from typing import Callable
from enum import Enum

class Language(Enum):
    PYTHON = "python"
    ELM = "elm"
    ELM_DECODERS = "elm_decoders"
    ELM_ENCODERS = "elm_encoders"

CLASS_NAME_MAPPING: dict[Language, Callable[[str], str]] = {
    Language.PYTHON: lambda name: name,
    Language.ELM: lambda name: name,
    Language.ELM_DECODERS: lambda name: name[:1].lower() + name[1:] + "Decoder",
    Language.ELM_ENCODERS: lambda name: name[:1].lower() + name[1:] + "Encoder",
}

def format_class_name(name: str, Language: Language) -> str:
    return CLASS_NAME_MAPPING[Language](name)
