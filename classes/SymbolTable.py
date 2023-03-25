class SymbolTable:
    symbols = {}

    @staticmethod
    def getter(identifier) -> int:
        if identifier in SymbolTable.symbols:
            return SymbolTable.symbols[identifier]
        raise NameError(f"name '{identifier}' is not defined")

    @staticmethod
    def setter(identifier, value) -> None:
        SymbolTable.symbols[identifier] = value
