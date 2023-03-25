from classes.Node import *
from classes.PrePro import PrePro, Tokenizer


class Parser:
    def parseBlock(self) -> Node:
        children = []
        while self.tokenizer.next.type != "EOF":
            children.append(self.parseStatement())
        return Block(children)

    def parseStatement(self) -> Node:
        node = NoOp()
        while self.tokenizer.next.type not in ["LN", "EOF"]:
            if self.tokenizer.next.type == "IDENTIFIER":
                idtf = self.tokenizer.next.value
                if idtf == "println":
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type != "PARENO":
                        raise SyntaxError("'(' needed")
                    self.tokenizer.selectNext()
                    node = Print("print", [self.parseExpression()])
                    if self.tokenizer.next.type != "PARENC":
                        raise SyntaxError("'(' was never closed")
                    self.tokenizer.selectNext()
                    continue

                self.tokenizer.selectNext()
                if self.tokenizer.next.type != "EQUALS":
                    raise SyntaxError("'=' needed")
                self.tokenizer.selectNext()
                node = Assignment(idtf, [self.parseExpression()])

        self.tokenizer.selectNext()
        return node

    def parseExpression(self) -> Node:
        fst_node = self.parseTerm()

        while self.tokenizer.next.type in ["PLUS", "MINUS"]:
            op = self.tokenizer.next.value
            self.tokenizer.selectNext()

            if self.tokenizer.next.type in ["DIV", "MULT"]:
                raise SyntaxError(f"ivalid syntax - {op}{self.tokenizer.next.value}")

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

            if self.tokenizer.next.type in ["DIV", "MULT"]:
                raise SyntaxError(f"ivalid syntax - {op}{self.tokenizer.next.value}")

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

        if self.tokenizer.next.type == "IDENTIFIER":
            val = self.tokenizer.next.value
            self.tokenizer.selectNext()
            return Identifier(val)

        if self.tokenizer.next.type in ["PLUS", "MINUS"]:
            op = self.tokenizer.next.value
            self.tokenizer.selectNext()

            if self.tokenizer.next.type in ["DIV", "MULT"]:
                raise SyntaxError(f"ivalid syntax - {op}{self.tokenizer.next.value}")

            return UnOp(op, [self.parseFactor()])

        if self.tokenizer.next.type == "PARENO":
            self.tokenizer.selectNext()
            node = self.parseExpression()
            if self.tokenizer.next.type == "PARENC":
                self.tokenizer.selectNext()
                return node
            raise SyntaxError("'(' was never closed")

    def run(self, code: str) -> any:
        pre_pro = PrePro()
        code = pre_pro.filter(code)
        self.tokenizer = Tokenizer(code)
        return self.parseBlock().evaluate()
