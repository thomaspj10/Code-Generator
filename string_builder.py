INDENT = "    "

class StringBuilder:
    
    __lines: list[str]

    def __init__(self) -> None:
        self.__lines = []

    def add_line(self, line: str, indent: int = 0):
        self.__lines.append((INDENT * indent) + line)

    def build(self) -> str:
        return "\n".join(self.__lines)