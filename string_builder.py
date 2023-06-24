DEFAULT_INDENT = "    "

class StringBuilder:
    
    __indent_str: str
    __lines: list[str]

    def __init__(self, indent_str: str = DEFAULT_INDENT) -> None:
        self.__lines = []
        self.__indent_str = indent_str

    def add_line(self, line: str, indent: int = 0):
        self.__lines.append((self.__indent_str * indent) + line)

    def build(self) -> str:
        return "\n".join(self.__lines)
