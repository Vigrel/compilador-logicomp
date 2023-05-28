from abc import ABC, abstractmethod
from typing import List
from classes.SymbolTable import SymbolTable
from classes.FuncTable import FuncTable


class Node(ABC):
    def __init__(self, value, children) -> None:
        self.value: any = value
        self.children: List[Node] = children

    @abstractmethod
    def evaluate(self, symbol_table: SymbolTable) -> any:
        return


class BinOp(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        rig = self.children[0].evaluate(symbol_table)
        lef = self.children[1].evaluate(symbol_table)

        if rig[0] == lef[0] and rig[0] == int:
            if self.value == "+":
                return (int, rig[1] + lef[1])
            if self.value == "-":
                return (int, rig[1] - lef[1])
            if self.value == "*":
                return (int, rig[1] * lef[1])
            if self.value == "/":
                return (int, rig[1] // lef[1])
            if self.value == "<":
                return (int, int(rig[1] < lef[1]))
            if self.value == ">":
                return (int, int(rig[1] > lef[1]))
            if self.value == "==":
                return (int, int(rig[1] == lef[1]))
            if self.value == "&&":
                return (int, int(rig[1] and lef[1]))
            if self.value == "||":
                return (int, int(rig[1] or lef[1]))

        if self.value == ".":
            return (str, str(rig[1]) + str(lef[1]))
        if self.value == "<":
            return (int, int(str(rig[1]) < str(lef[1])))
        if self.value == ">":
            return (int, int(str(rig[1]) > str(lef[1])))
        if self.value == "==":
            return (int, int(str(rig[1]) == str(lef[1])))
        if self.value == "&&":
            return (str, str(rig[1]) and str(lef[1]))
        if self.value == "||":
            return (str, str(rig[1]) or str(lef[1]))

        raise TypeError(
            f"unsupported operand type(s) for {self.value}: '{rig[0]}' and '{lef[0]}'"
        )


class UnOp(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        eva = self.children[0].evaluate(symbol_table)
        if self.value == "!":
            return (eva[0], not eva[1])
        if self.value == "-":
            return (eva[0], -eva[1])
        return (eva[0], eva[1])


class IntVal(Node):
    def __init__(self, value: int) -> None:
        super().__init__(int(value), [])

    def evaluate(self, symbol_table: SymbolTable) -> int:
        return (int, self.value)


class NoOp(Node):
    def __init__(self) -> None:
        super().__init__(0, [])

    def evaluate(self, symbol_table: SymbolTable) -> None:
        return None


class Print(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self, symbol_table: SymbolTable) -> None:
        print(self.children[0].evaluate(symbol_table)[1])


class Identifier(Node):
    def __init__(self, value) -> None:
        super().__init__(value, [])

    def evaluate(self, symbol_table) -> int:
        if self.value in symbol_table.reserved:
            return self.value
        return symbol_table.getter(self.value)


class Assignment(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        symbol_table.setter(self.value, self.children[0].evaluate(symbol_table))


class Block(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self, symbol_table: SymbolTable):
        for child in self.children:
            if type(child) == Return:
                return child.evaluate(symbol_table)
            child.evaluate(symbol_table)


class ReadLn(Node):
    def __init__(self) -> None:
        super().__init__(0, [])

    def evaluate(self, symbol_table: SymbolTable) -> int:
        return (int, int(input()))


class While(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self, symbol_table: SymbolTable) -> None:
        while self.children[0].evaluate(symbol_table)[1]:
            self.children[1].evaluate(symbol_table)


class If(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self, symbol_table: SymbolTable) -> None:
        if self.children[0].evaluate(symbol_table)[1]:
            return self.children[1].evaluate(symbol_table)
        if len(self.children) == 3:
            return self.children[2].evaluate(symbol_table)


class VarDec(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        symbol_table.create(self.value, self.children[0].evaluate(symbol_table))
        if len(self.children) == 2:
            symbol_table.setter(self.value, self.children[1].evaluate(symbol_table))


class FuncDec(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        FuncTable.create(self.value, self)


class FuncCall(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self, symbol_table: SymbolTable):
        function = FuncTable.getter(self.value)
        func_st = SymbolTable()
        for arg, value in zip(function[1].children[1], self.children):
            func_st.create(arg[0], arg[1])
            func_st.setter(arg[0], value.evaluate(symbol_table))

        result = function[1].children[2].evaluate(func_st)
        if result == None:
            result = (int, 1)
        if function[0] != result[0]:
            raise SyntaxError

        return result


class StrVal(Node):
    def __init__(self, value: str) -> None:
        super().__init__(str(value), [])

    def evaluate(self, symbol_table: SymbolTable) -> str:
        return (str, self.value)


class Return(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self, symbol_table: SymbolTable) -> None:
        return self.children[0].evaluate(symbol_table)
