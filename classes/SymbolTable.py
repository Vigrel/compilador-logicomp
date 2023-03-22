class SymbolTable:
    symbols = {}

    @staticmethod
    def getter(identifier) -> int:
        try:
            return SymbolTable.symbols[identifier]
        except:
            raise KeyError(identifier)

    @staticmethod
    def setter(identifier, value) -> None:
        SymbolTable.symbols[identifier] = value
