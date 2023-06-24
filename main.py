from builders.class_builder import class_builder
from language import Language
from type import Type

cls = (
    class_builder()
    .name("Person")
    .attribute("name", Type.STRING)
    .attribute("age", Type.INT)
    .build(Language.ELM)
)

print(cls)
