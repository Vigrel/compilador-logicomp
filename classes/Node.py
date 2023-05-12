from abc import ABC, abstractmethod
from typing import List
import uuid

from classes.SymbolTable import SymbolTable
from classes.WriteNASM import WriteNASM


class Node(ABC):
    def __init__(self, value, children) -> None:
        self.value: any = value
        self.children: List[Node] = children
        self.id = int(uuid.uuid1())

    @abstractmethod
    def evaluate(self) -> any:
        return


class BinOp(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self):
        lef = self.children[0].evaluate()
        WriteNASM.write("\nPUSH EBX")
        rig = self.children[1].evaluate()

        WriteNASM.write("\nPOP EAX")
        if self.value == "+":
            WriteNASM.write("\nADD EAX, EBX")
            WriteNASM.write("\nMOV EBX, EAX")
            return lef + rig
        if self.value == "-":
            WriteNASM.write("\nSUB EAX, EBX")
            WriteNASM.write("\nMOV EBX, EAX")
            return lef - rig
        if self.value == "*":
            WriteNASM.write("\nIMUL EBX")
            WriteNASM.write("\nMOV EBX, EAX")
            return lef * rig
        if self.value == "/":
            WriteNASM.write("\nDIV EAX, EBX")
            WriteNASM.write("\nMOV EBX, EAX")
            return lef // rig
        if self.value == "<":
            WriteNASM.write("\nCMP EAX, EBX")
            WriteNASM.write("\nCALL binop_jl")
            return int(lef < rig)
        if self.value == ">":
            WriteNASM.write("\nCMP EAX, EBX")
            WriteNASM.write("\nCALL binop_jg")
            return int(lef > rig)
        if self.value == "==":
            WriteNASM.write("\nCMP EAX, EBX")
            WriteNASM.write("\nCALL binop_je")
            return int(lef == rig)

        raise TypeError(
            f"unsupported operand type(s) for {self.value}: '{rig[0]}' and '{lef[0]}'"
        )


class UnOp(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self):
        eva = self.children[0].evaluate()
        if self.value == "-":
            return -eva
        return eva


class IntVal(Node):
    def __init__(self, value: int) -> None:
        super().__init__(int(value), [])

    def evaluate(self) -> int:
        WriteNASM.write(f"\nMOV EBX, {self.value}")
        return self.value


class NoOp(Node):
    def __init__(self) -> None:
        super().__init__(0, [])

    def evaluate(self) -> None:
        return None


class Print(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self) -> None:
        print(self.children[0].evaluate())
        WriteNASM.write("\nPUSH EBX")
        WriteNASM.write("\nCALL print")
        WriteNASM.write("\nPOP EBX")


class Identifier(Node):
    def __init__(self, value) -> None:
        super().__init__(value, [])

    def evaluate(self) -> int:
        WriteNASM.write(f"\nMOV EBX, [EBP-{SymbolTable.getter(self.value)[0]}]")
        return SymbolTable.getter(self.value)[1]


class Assignment(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self):
        SymbolTable.setter(self.value, self.children[0].evaluate())
        WriteNASM.write(f"\nMOV [EBP-{SymbolTable.getter(self.value)[0]}], EBX")


class Block(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self) -> None:
        for child in self.children:
            child.evaluate()


class While(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self) -> None:
        WriteNASM.write(f"\nLOOP_{self.id}:")
        self.children[0].evaluate()
        WriteNASM.write(f"\nCMP EBX, False")
        WriteNASM.write(f"\nJE EXIT_{self.id}")
        self.children[1].evaluate()
        WriteNASM.write(f"\nJMP LOOP_{self.id}")
        WriteNASM.write(f"\nEXIT_{self.id}:")


class If(Node):
    def __init__(self, children) -> None:
        super().__init__(0, children)

    def evaluate(self) -> None:
        WriteNASM.write(f"\nCMP EBX, False")
        WriteNASM.write(f"\nJE IF_{self.id}")
        if len(self.children) == 3:
            self.children[2].evaluate()
        WriteNASM.write(f"\nIF_{self.id}:")
        self.children[1].evaluate()


class VarDec(Node):
    def __init__(self, value, children) -> None:
        super().__init__(value, children)

    def evaluate(self):
        WriteNASM.write("\nPUSH DWORD 0")
        SymbolTable.create(self.value)
        if len(self.children) == 2:
            SymbolTable.setter(self.value, self.children[1].evaluate())


class ReadLn(Node):
    def __init__(self) -> None:
        super().__init__(0, [])

    def evaluate(self) -> int:
        return int(input())


class StrVal(Node):
    def __init__(self, value: str) -> None:
        super().__init__(str(value), [])

    def evaluate(self) -> str:
        return (str, self.value)
