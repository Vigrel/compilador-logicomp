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

    def evaluate(self) -> int:
        if self.value == "+":
            return self.children[0].evaluate() + self.children[1].evaluate()
        if self.value == "-":
            return self.children[0].evaluate() - self.children[1].evaluate()
        if self.value == "*":
            return self.children[0].evaluate() * self.children[1].evaluate()
        if self.value == "/":
            return self.children[0].evaluate() // self.children[1].evaluate()
        if self.value == "<":
            return self.children[0].evaluate() < self.children[1].evaluate()
        if self.value == ">":
            return self.children[0].evaluate() > self.children[1].evaluate()
        if self.value == "&&":
            return self.children[0].evaluate() and self.children[1].evaluate()
        if self.value == "||":
            return self.children[0].evaluate() or self.children[1].evaluate()
        if self.value == "==":
            return self.children[0].evaluate() == self.children[1].evaluate()


class UnOp(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self) -> any:
        if self.value == "!":
            return not self.children[0].evaluate()
        if self.value == "-":
            return -self.children[0].evaluate()
        return self.children[0].evaluate()


class IntVal(Node):
    def __init__(self, value: int) -> None:
        super().__init__(int(value), [])

    def evaluate(self) -> int:
        return self.value


class NoOp(Node):
    def __init__(self) -> None:
        super().__init__(0, [])

    def evaluate(self) -> None:
        return None


class Print(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self) -> None:
        print(self.children[0].evaluate())


class Identifier(Node):
    def __init__(self, value) -> None:
        super().__init__(value, [])

    def evaluate(self) -> int:
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
        return int(input())


class While(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self) -> None:
        while self.children[0].evaluate():
            self.children[1].evaluate()


class If(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self) -> None:
        if self.children[0].evaluate():
            return self.children[1].evaluate()
        if len(self.children) == 3:
            return self.children[2].evaluate()
