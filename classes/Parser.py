from classes.Tokenizer import Tokenizer
from classes.PrePro import PrePro
from classes.Node import Node, BinOp, UnOp, IntVal


class Parser:
    def parseExpression(self) -> Node:
        fst_node = self.parseTerm()

        while self.tokenizer.next.type in ["PLUS", "MINUS"]:
            op = self.tokenizer.next.value
            self.tokenizer.selectNext()
            scd_node = BinOp(
                op,
                [fst_node, self.parseTerm()],
            )
            fst_node = scd_node

        return fst_node

    def parseTerm(self) -> Node:
        fst_node = self.parseFactor()

        while self.tokenizer.next.type in ["DIV", "MULT"]:
            op = self.tokenizer.next.value
            self.tokenizer.selectNext()
            scd_node = BinOp(
                op,
                [fst_node, self.parseFactor()],
            )
            fst_node = scd_node

        return fst_node

    def parseFactor(self) -> Node:
        if self.tokenizer.next.type == "INT":
            val = self.tokenizer.next.value
            self.tokenizer.selectNext()
            return IntVal(val)

        if self.tokenizer.next.type in ["PLUS", "MINUS"]:
            op = self.tokenizer.next.value
            self.tokenizer.selectNext()
            return UnOp(op, [self.parseFactor()])

        if self.tokenizer.next.type == "PARENO":
            self.tokenizer.selectNext()
            node = self.parseExpression()
            if self.tokenizer.next.type == "PARENC":
                self.tokenizer.selectNext()
                return node
            raise KeyError

    def run(self, file: str) -> int:
        with open(file, "r") as f:
            code = f.read()

        pre_pro = PrePro()
        code = pre_pro.filter(code)

        self.tokenizer = Tokenizer(code)
        result = self.parseExpression().evaluate()

        if self.tokenizer.next.type != "EOF":
            raise KeyError

        return result
