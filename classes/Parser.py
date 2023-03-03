from classes.Tokenizer import Tokenizer
from classes.PrePro import PrePro


class Parser:
    def parseTerm(self) -> int:
        if self.tokenizer.next.type == "INT":
            result = int(self.tokenizer.next.value)
            self.tokenizer.selectNext()

            while self.tokenizer.next.type in ["MULT", "DIV"]:
                if self.tokenizer.next.type == "MULT":
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "INT":
                        result *= int(self.tokenizer.next.value)
                    else:
                        raise KeyError

                if self.tokenizer.next.type == "DIV":
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "INT":
                        result //= int(self.tokenizer.next.value)
                    else:
                        raise KeyError

                self.tokenizer.selectNext()

            return result

        raise KeyError

    def parseExpression(self) -> int:
        result = self.parseTerm()

        while self.tokenizer.next.type in ["PLUS", "MINUS"]:
            if self.tokenizer.next.type == "PLUS":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "INT":
                    result += self.parseTerm()
                else:
                    raise KeyError

            if self.tokenizer.next.type == "MINUS":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "INT":
                    result -= self.parseTerm()
                else:
                    raise KeyError

            self.tokenizer.selectNext()

            if self.tokenizer.next.type == "EOF":
                return result

        raise KeyError

    def run(self, code: str) -> None:
        pre_pro: PrePro = PrePro()
        code = pre_pro.filter(code)
        self.tokenizer: Tokenizer = Tokenizer(code)

        return self.parseExpression()
