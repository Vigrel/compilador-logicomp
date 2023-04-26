class SymbolTable:
    reserved = {"while", "if", "Int", "String", "println", "readline"}
    symbols = {}

    @staticmethod
    def create(identifier, type):
        if identifier in SymbolTable.symbols:
            raise NameError(f"name '{identifier}' already exist")
        if type == "Int":
            SymbolTable.symbols[identifier] = (int, 0)
            return
        if type == "String":
            SymbolTable.symbols[identifier] = (str, "")
            return
        raise NameError(f"type '{type}' doesn't exist")

    @staticmethod
    def getter(identifier) -> int:
        if identifier in SymbolTable.symbols:
            return SymbolTable.symbols[identifier]
        raise NameError(f"name '{identifier}' is not defined")

    @staticmethod
    def setter(identifier, value) -> None:
        if SymbolTable.symbols[identifier][0] == value[0] and value[0] == int:
            SymbolTable.symbols[identifier] = (
                SymbolTable.symbols[identifier][0],
                value[1],
            )
        if SymbolTable.symbols[identifier][0] == value[0] and value[0] == str:
            SymbolTable.symbols[identifier] = (
                SymbolTable.symbols[identifier][0],
                value[1],
            )
