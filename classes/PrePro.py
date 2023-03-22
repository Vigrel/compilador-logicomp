import re

OPS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULT",
    "/": "DIV",
    "(": "PARENO",
    ")": "PARENC",
    "=": "EQUALS",
}


class PrePro:
    @staticmethod
    def filter(code: str) -> str:
        try:
            return re.match("(.*?)#", code).group()[:-1]
        except:
            return code


class Token:
    def __init__(self, type: str, value: int) -> None:
        self.type: str = type
        self.value: int = value


class Tokenizer:
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.position: int = 0
        self.next: Token = self.selectNext()

    def selectNext(self) -> Token:
        for letter in self.source[self.position :]:
            if letter == " ":
                self.position += 1
                continue

            if letter in OPS.keys():
                self.next = Token(OPS[letter], letter)
                self.position += 1
                return self.next

            if letter.isdigit():
                num = ""
                while letter.isdigit():
                    num += letter
                    self.position += 1
                    if self.position == len(self.source):
                        break
                    letter = self.source[self.position]
                self.next = Token("INT", num)
                return self.next

            if letter.isalpha() or letter == "_":
                num = ""
                while letter.isdigit() or letter.isalpha() or "_":
                    num += letter
                    self.position += 1
                    if self.position == len(self.source):
                        break
                    letter = self.source[self.position]
                self.next = Token("IDENTIFIER", num)
                return self.next

            if letter == "\\":
                self.position += 1
                if self.source[self.position] == "n":
                    self.next = Token("LN", "\\n")
                    self.position += 1
                    return self.next
                raise SyntaxError(f"invalid syntax - \\{self.source[self.position]}")

            raise SyntaxError(f"invalid syntax - {self.source[self.position]}")

        self.next = Token("EOF", "")
        return self.next
