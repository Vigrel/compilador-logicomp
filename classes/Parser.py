from classes.Token import Token
from classes.Tokenizer import Tokenizer

from constants.grammar import OPS


class Parser:
    def parseExpression(self) -> Token:
        pass

    def run(self, code: str) -> None:
        self.tokenizer: Tokenizer = Tokenizer(code)

        if self.tokenizer.next.type == "INT":
            result = int(self.tokenizer.next.value)
            self.tokenizer.selectNext()

            while self.tokenizer.next.type in OPS.values():
                if self.tokenizer.next.type == "PLUS":
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "INT":
                        result += int(self.tokenizer.next.value)
                    else:
                        raise KeyError

                if self.tokenizer.next.type == "MINUS":
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "INT":
                        result -= int(self.tokenizer.next.value)
                    else:
                        raise KeyError

                self.tokenizer.selectNext()

            if self.tokenizer.next.type == "EOF":
                return result
        raise KeyError
