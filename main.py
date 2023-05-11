import sys

from classes.Parser import Parser
from classes.WriteNASM import WriteNASM

if __name__ == "__main__":
    with open(sys.argv[1:][0], "r") as f:
        code = f.read()

    WriteNASM.file_name = f"{sys.argv[1:][0][:-3]}.asm"
    WriteNASM.start()
    Parser.run(code)
    WriteNASM.close()
