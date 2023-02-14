import sys

from classes.Parser import Parser

if __name__ == "__main__":
    parser = Parser()
    print(parser.run(sys.argv[1:][0]))
