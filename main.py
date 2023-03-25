import sys

from classes.Parser import Parser

if __name__ == "__main__":
    with open(sys.argv[1:][0], "r") as f:
        code = f.read()

    parser = Parser()
    parser.run(code)
