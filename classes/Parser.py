from classes.Node import *
from classes.PrePro import Tokenizer


class Parser:
    tknz = Tokenizer("")

    @staticmethod
    def parseBlock() -> Node:
        children = []
        while Parser.tknz.next.type != "EOF":
            children.append(Parser.parseStatement())
        return Block(children)

    @staticmethod
    def parseStatement() -> Node:
        node = NoOp()
        while Parser.tknz.next.type not in ["LN", "EOF"]:
            if Parser.tknz.next.type == "IDENTIFIER":
                idtf = Parser.tknz.next.value
                if idtf == "println":
                    Parser.tknz.selectNext()
                    if Parser.tknz.next.type != "PARENO":
                        raise SyntaxError("'(' needed")
                    Parser.tknz.selectNext()
                    node = Print("print", [Parser.parseExpression()])
                    if Parser.tknz.next.type != "PARENC":
                        raise SyntaxError("'(' was never closed")
                    Parser.tknz.selectNext()
                    continue

                Parser.tknz.selectNext()
                if Parser.tknz.next.type != "EQUALS":
                    raise SyntaxError("'=' needed")
                Parser.tknz.selectNext()
                node = Assignment(idtf, [Parser.parseExpression()])
                continue
            raise SyntaxError(f"ivalid syntax - {Parser.tknz.next.value}")

        Parser.tknz.selectNext()
        return node

    @staticmethod
    def parseExpression() -> Node:
        node = Parser.parseTerm()

        while Parser.tknz.next.type in ["PLUS", "MINUS"]:
            op = Parser.tknz.next.value
            Parser.tknz.selectNext()

            if Parser.tknz.next.type in ["DIV", "MULT"]:
                raise SyntaxError(f"ivalid syntax - {op}{Parser.tknz.next.value}")

            node = BinOp(
                op,
                [node, Parser.parseTerm()],
            )

        return node

    @staticmethod
    def parseTerm() -> Node:
        node = Parser.parseFactor()

        while Parser.tknz.next.type in ["DIV", "MULT"]:
            op = Parser.tknz.next.value
            Parser.tknz.selectNext()

            if Parser.tknz.next.type in ["DIV", "MULT"]:
                raise SyntaxError(f"ivalid syntax - {op}{Parser.tknz.next.value}")

            node = BinOp(
                op,
                [node, Parser.parseFactor()],
            )

        return node

    @staticmethod
    def parseFactor() -> Node:
        tkn = Parser.tknz.next
        Parser.tknz.selectNext()

        if tkn.type == "INT":
            return IntVal(tkn.value)

        if tkn.type == "IDENTIFIER":
            return Identifier(tkn.value)

        if tkn.type in ["PLUS", "MINUS"]:
            if Parser.tknz.next.type in ["DIV", "MULT"]:
                raise SyntaxError(
                    f"ivalid syntax - {tkn.value}{Parser.tknz.next.value}"
                )

            return UnOp(tkn.value, [Parser.parseFactor()])

        if tkn.type == "PARENO":
            node = Parser.parseExpression()
            if Parser.tknz.next.type == "PARENC":
                Parser.tknz.selectNext()
                return node
            raise SyntaxError("'(' was never closed")

    @staticmethod
    def run(code: str) -> any:
        Parser.tknz.__init__(code)

        return Parser.parseBlock().evaluate()
