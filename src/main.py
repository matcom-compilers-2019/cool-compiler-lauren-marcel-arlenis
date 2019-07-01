from cool_compiler import Compiler
import sys

if __name__ == "__main__":
    file_name = sys.argv[1]

    compilador = Compiler()
    compilador.compile(file_name)