from classes.Tokenizer import Tokenizer
from classes.Token import Token
from classes.PrePro import PrePro


class Parser:
    def parseTerm(self) -> int:
        result = self.parseFactor()
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
        print(act_tkn.type)
        print(act_tkn.value)
        if act_tkn.type == "PARENO":
            result = self.parseExpression()
            if self.tokenizer.next.type != "PARENC":
                raise KeyError
            self.tokenizer.selectNext()
            return result

        if act_tkn.type == "INT":
            return int(act_tkn.value)

        if act_tkn.type == "MINUS":
            if self.tokenizer.next.type == "PLUS":
                self.tokenizer.next = Token("MINUS", "-")
                return self.parseFactor()

            if self.tokenizer.next.type == "MINUS":
                self.tokenizer.next = Token("PLUS", "+")
                return self.parseFactor()

            if self.tokenizer.next.type == "INT":
                result = self.tokenizer.next.value
                self.tokenizer.selectNext()
                return -int(result)

        if act_tkn.type == "PLUS":
            if self.tokenizer.next.type == "INT":
                result = self.tokenizer.next.value
                self.tokenizer.selectNext()
                return int(result)
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

        if self.tokenizer.next.type == "INT":
            raise KeyError

        return result

    def run(self, code: str) -> None:
        pre_pro: PrePro = PrePro()
        code = pre_pro.filter(code)
        self.tokenizer: Tokenizer = Tokenizer(code)
        return self.parseExpression()
