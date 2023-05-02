from abc import ABC, abstractmethod
from typing import List
from classes.SymbolTable import SymbolTable


class Node(ABC):
    def __init__(self, value, children) -> None:
        self.value: any = value
        self.children: List[Node] = children

    @abstractmethod
    def evaluate(self) -> any:
        return


class BinOp(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self):
        rig = self.children[0].evaluate()
        lef = self.children[1].evaluate()

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

    def evaluate(self):
        eva = self.children[0].evaluate()
        if self.value == "!":
            return (eva[0], not eva[1])
        if self.value == "-":
            return (eva[0], -eva[1])
        return (eva[0], eva[1])


class IntVal(Node):
    def __init__(self, value: int) -> None:
        super().__init__(int(value), [])

    def evaluate(self) -> int:
        return (int, self.value)


class NoOp(Node):
    def __init__(self) -> None:
        super().__init__(0, [])

    def evaluate(self) -> None:
        return None


class Print(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self) -> None:
        print(self.children[0].evaluate()[1])


class Identifier(Node):
    def __init__(self, value) -> None:
        super().__init__(value, [])

    def evaluate(self) -> int:
        if self.value in SymbolTable.reserved:
            return self.value
        return SymbolTable.getter(self.value)


class Assignment(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self):
        SymbolTable.setter(self.value, self.children[0].evaluate())


class Block(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self) -> None:
        for child in self.children:
            child.evaluate()


class ReadLn(Node):
    def __init__(self) -> None:
        super().__init__(0, [])

    def evaluate(self) -> int:
        return (int, int(input()))


class While(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self) -> None:
        while self.children[0].evaluate()[1]:
            self.children[1].evaluate()


class If(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self) -> None:
        if self.children[0].evaluate()[1]:
            return self.children[1].evaluate()
        if len(self.children) == 3:
            return self.children[2].evaluate()


class VarDec(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self):
        SymbolTable.create(self.value, self.children[0].evaluate())
        if len(self.children) == 2:
            SymbolTable.setter(self.value, self.children[1].evaluate())


class StrVal(Node):
    def __init__(self, value: str) -> None:
        super().__init__(str(value), [])

    def evaluate(self) -> str:
        return (str, self.value)
