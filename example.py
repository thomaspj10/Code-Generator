from builders import class_builder, file_builder
from language import Language
from type import Type

address = (
    class_builder("Address")
    .attribute("street", Type.STRING)
    .attribute("number", Type.INT)
)

person = (
    class_builder("Person")
    .attribute("name", Type.STRING)
    .attribute("age", Type.INT)
    .attribute("address", Type.LIST, [address])
    .attribute("names", Type.LIST, [Type.STRING])
)

builder = file_builder().add(person)

builder.save("Types.elm", "./elm/src/", Language.ELM)
builder.save("types.py", "./python/", Language.PYTHON)
