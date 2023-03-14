from abc import ABC, abstractmethod
from typing import List


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


class UnOp(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self) -> any:
        if self.value == "-":
            return -self.children[0].evaluate()
        return self.children[0].evaluate()


class IntVal(Node):
    def __init__(self, value: int) -> None:
        super().__init__(int(value), [])

    def evaluate(self) -> int:
        return self.value


class NoOp(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self) -> None:
        return None
