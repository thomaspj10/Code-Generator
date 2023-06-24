from builders import class_builder, file_builder
from language import Language
from type import Type

cls = (
    class_builder()
    .name("Person")
    .attribute("name", Type.STRING)
    .attribute("age", Type.INT)
)

file_builder("Types.elm").add(cls).save("./elm/src/", Language.ELM)
file_builder("types.py").add(cls).save("./python/", Language.PYTHON)

