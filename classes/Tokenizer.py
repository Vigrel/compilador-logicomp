from classes.Token import Token
from constants.grammar import INT, OPS


class Tokenizer:
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.position: int = 0
        self.next: Token = self.selectNext()

    def selectNext(self) -> Token:
        for letter in self.source[self.position :]:
            if letter in OPS.keys():
                self.next = Token(OPS[letter], letter)
                self.position += 1
                return self.next

            if letter in INT:
                num = ""
                while letter in INT:
                    num += letter
                    self.position += 1
                    if self.position == len(self.source):
                        break
                    letter = self.source[self.position]
                self.next = Token("INT", num)
                return self.next

            if letter == " ":
                self.position += 1
                continue

            raise KeyError

        self.next = Token("EOF", "")
        return self.next
