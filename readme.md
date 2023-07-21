## Installing
```
pip install -e .
```

## Usage
```py
import codegen.codegenerator as cg

person = (
    cg.dto("Person")
    .attribute("id", cg.Type.INT)
    .attribute("name", cg.Type.STRING)
)

cg.store_python("types.py")
cg.store_elm("Types.elm")
```
