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

file_builder("Types.elm").add(person_cls).add(address_cls).save("./elm/src/", Language.ELM)
file_builder("types.py").add(person_cls).add(address_cls).save("./python/", Language.PYTHON)
