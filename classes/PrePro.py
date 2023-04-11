import re

OPS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULT",
    "/": "DIV",
    "(": "PARENO",
    ")": "PARENC",
    "!": "NOT",
    ">": "GT",
    "<": "LT",
}


class PrePro:
    @staticmethod
    def filter(code: str) -> str:
        return re.sub(r"\s*#.*$", "", code, flags=re.MULTILINE)


class Token:
    def __init__(self, type: str, value: int) -> None:
        self.type: str = type
        self.value: int = value


class Tokenizer:
    def __init__(self, source: str) -> None:
        self.source: str = PrePro.filter(source)
        self.position: int = 0
        self.next: Token = Token("", 0)
        self.length = len(self.source)

        self.selectNext()

    def selectNext(self):
        while self.position < self.length:
            letter = self.source[self.position]
            self.position += 1

            if letter == " ":
                continue

            elif letter in OPS:
                self.next = Token(OPS[letter], letter)

            elif letter in ["|", "&", "="]:
                symbol = letter
                while self.position < self.length and self.source[self.position] in [
                    "|",
                    "&",
                    "=",
                    " ",
                ]:
                    if self.source[self.position] == symbol:
                        if symbol == "&":
                            self.next = Token("AND", f"&&")
                        if symbol == "|":
                            self.next = Token("OR", f"||")
                        if symbol == "=":
                            self.next = Token("EQUALSS", f"==")
                        self.position += 1
                        break
                    self.position += 1
                else:
                    if symbol == "=":
                        self.next = Token("EQUALS", f"=")
                    else:
                        raise SyntaxError(
                            f"invalid syntax - {self.source[self.position - 1]}"
                        )

            elif letter.isdecimal():
                num = letter
                while (
                    self.position < self.length
                    and self.source[self.position].isdecimal()
                ):
                    num += self.source[self.position]
                    self.position += 1
                self.next = Token("INT", num)

            elif letter.isalpha() or letter == "_":
                idtf = letter
                while self.position < self.length and (
                    self.source[self.position].isalnum()
                    or self.source[self.position] == "_"
                ):
                    idtf += self.source[self.position]
                    self.position += 1
                self.next = Token("IDENTIFIER", idtf)

            elif letter == "\n":
                self.next = Token("LN", "\n")

            else:
                raise SyntaxError(f"invalid syntax - {self.source[self.position]}")
            return

        self.next = Token("EOF", "")
