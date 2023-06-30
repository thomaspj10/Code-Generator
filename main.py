from builders import class_builder, file_builder
from language import Language
from type import Type

address_cls = (
    class_builder()
    .name("Address")
    .attribute("street", Type.STRING)
    .attribute("number", Type.INT)
)

person_cls = (
    class_builder()
    .name("Person")
    .attribute("name", Type.STRING)
    .attribute("age", Type.INT)
    .attribute("address", address_cls)
)

builder = file_builder().add(person_cls)

builder.save("Types.elm", "./elm/src/", Language.ELM)
builder.save("types.py", "./python/", Language.PYTHON)
