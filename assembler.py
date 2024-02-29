import sys

from compiler import Program
from linker import Linker
from output import print_output


def parse_file(file) -> Program:
    program = Program()

    with open(file, "r") as source:
        line = source.readline()

        while line:
            program.next_instruction(line)
            line = source.readline()

    return program


if __name__ == '__main__':
    assert len(sys.argv) > 1, "No file provided. Please provide a file path."

    program = parse_file(sys.argv[1])
    labels = program.labels()
    bytecode = program.bytecode()

    start_pos = 0xC000
    bytecode = Linker(start_pos).parse(labels, bytecode)

    print_output(labels, bytecode, start_pos, bytes_per_line=8)
