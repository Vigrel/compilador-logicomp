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

        Parser.tknz.selectNext()
        return node

    @staticmethod
    def parseExpression() -> Node:
        fst_node = Parser.parseTerm()

        while Parser.tknz.next.type in ["PLUS", "MINUS"]:
            op = Parser.tknz.next.value
            Parser.tknz.selectNext()

            if Parser.tknz.next.type in ["DIV", "MULT"]:
                raise SyntaxError(f"ivalid syntax - {op}{Parser.tknz.next.value}")

            scd_node = BinOp(
                op,
                [fst_node, Parser.parseTerm()],
            )
            fst_node = scd_node

        return fst_node

    @staticmethod
    def parseTerm() -> Node:
        fst_node = Parser.parseFactor()

        while Parser.tknz.next.type in ["DIV", "MULT"]:
            op = Parser.tknz.next.value
            Parser.tknz.selectNext()

            if Parser.tknz.next.type in ["DIV", "MULT"]:
                raise SyntaxError(f"ivalid syntax - {op}{Parser.tknz.next.value}")

            scd_node = BinOp(
                op,
                [fst_node, Parser.parseFactor()],
            )
            fst_node = scd_node

        return fst_node

    @staticmethod
    def parseFactor() -> Node:
        if Parser.tknz.next.type == "INT":
            val = Parser.tknz.next.value
            Parser.tknz.selectNext()
            return IntVal(val)

        if Parser.tknz.next.type == "IDENTIFIER":
            val = Parser.tknz.next.value
            Parser.tknz.selectNext()
            return Identifier(val)

        if Parser.tknz.next.type in ["PLUS", "MINUS"]:
            op = Parser.tknz.next.value
            Parser.tknz.selectNext()

            if Parser.tknz.next.type in ["DIV", "MULT"]:
                raise SyntaxError(f"ivalid syntax - {op}{Parser.tknz.next.value}")

            return UnOp(op, [Parser.parseFactor()])

        if Parser.tknz.next.type == "PARENO":
            Parser.tknz.selectNext()
            node = Parser.parseExpression()
            if Parser.tknz.next.type == "PARENC":
                Parser.tknz.selectNext()
                return node
            raise SyntaxError("'(' was never closed")

    @staticmethod
    def run(code: str) -> any:
        Parser.tknz.__init__(code)

        # while Parser.tknz.next.type != "EOF":
        #     # print(Parser.tknz.next.type)
        #     # print(Parser.tknz.next.value)
        #     Parser.tknz.selectNext()

        return Parser.parseBlock().evaluate()
