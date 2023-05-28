class FuncTable:
    functions = {}

    @staticmethod
    def create(value, children):
        if children.children[0] in FuncTable.functions:
            raise NameError(f"name '{children.children[0]}' already exist")
        if value == "Int":
            FuncTable.functions[children.children[0]] = (int, children)
            return
        if value == "String":
            FuncTable.functions[children.children[0]] = (str, children)
            return
        raise NameError(f"type '{value}' doesn't exist")

    @staticmethod
    def getter(identifier) -> int:
        if identifier in FuncTable.functions:
            return FuncTable.functions[identifier]
        raise NameError(f"name '{identifier}' is not defined")
