from classes.Tokenizer import Tokenizer
from classes.Token import Token
from classes.PrePro import PrePro


class Parser:
    def parseTerm(self) -> int:
        result = self.parseFactor()
        print(result)
        print(self.tokenizer.next.type)
        print(self.tokenizer.next.value)
        while self.tokenizer.next.type in ["MULT", "DIV"]:
            if self.tokenizer.next.type == "MULT":
                self.tokenizer.selectNext()
                result *= self.parseFactor()
                continue

            if self.tokenizer.next.type == "DIV":
                self.tokenizer.selectNext()
                result //= self.parseFactor()
                continue

            self.tokenizer.selectNext()

        return result

    def parseFactor(self) -> int:
        act_tkn = self.tokenizer.next
        self.tokenizer.selectNext()

        if act_tkn.type == "INT":
            return int(act_tkn.value)

        if self.tokenizer.next.type == "INT":
            result = self.tokenizer.next.value
            self.tokenizer.selectNext()
            if act_tkn.type == "MINUS":
                return -int(result)
            return int(result)

        if act_tkn.type == "MINUS":
            if self.tokenizer.next.type == "PLUS":
                self.tokenizer.next = Token("MINUS", "-")
                return self.parseFactor()

            if self.tokenizer.next.type == "MINUS":
                self.tokenizer.next = Token("PLUS", "+")
                return self.parseFactor()
            return self.parseFactor()

        if act_tkn.type == "PLUS":
            return self.parseFactor()

        raise KeyError

    def parseExpression(self) -> int:
        result = self.parseTerm()
        while self.tokenizer.next.type in ["PLUS", "MINUS"]:
            if self.tokenizer.next.type == "PLUS":
                self.tokenizer.selectNext()
                result += self.parseTerm()
                continue

            if self.tokenizer.next.type == "MINUS":
                self.tokenizer.selectNext()
                result -= self.parseTerm()
                continue

            self.tokenizer.selectNext()

        if self.tokenizer.next.type == "EOF":
            return result

        raise KeyError

    def run(self, code: str) -> None:
        pre_pro: PrePro = PrePro()
        code = pre_pro.filter(code)
        self.tokenizer: Tokenizer = Tokenizer(code)
        return self.parseExpression()
