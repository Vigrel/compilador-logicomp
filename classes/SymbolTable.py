class SymbolTable:
    symbols = {}

    @staticmethod
    def create(identifier):
        if identifier in SymbolTable.symbols:
            raise NameError(f"name '{identifier}' already exist")
        SymbolTable.symbols[identifier] = (len(SymbolTable.symbols) * 4 + 4, "")

    @staticmethod
    def getter(identifier) -> int:
        if identifier not in SymbolTable.symbols:
            raise NameError(f"name '{identifier}' is not defined")
        return SymbolTable.symbols[identifier]

    @staticmethod
    def setter(identifier, value) -> None:
        SymbolTable.symbols[identifier] = (SymbolTable.getter(identifier)[0], value)
