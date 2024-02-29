from argparse import ArgumentParser

from src.compiler import Program
from src.linker import Linker
from src.output import print_output


def arguments():
    parser = ArgumentParser(
        prog="Danmos Assembler",
        description=" A simple, basic, uncompleted 6502 assembler",
    )

    parser.add_argument('filename')
    parser.add_argument(
        '-s',
        '--start-position',
        help="Start position of the program (hexidecimal) [default: 0xC000]",
        default="C000"
    )
    parser.add_argument(
        '-b',
        '--bytes-per-line',
        help="Number of bytes per line in instructions output [default: 8]",
        default="8"
    )

    return parser.parse_args()


def parse_file(file) -> Program:
    program = Program()

    with open(file, "r") as source:
        line = source.readline()

        while line:
            program.next_instruction(line)
            line = source.readline()

    return program


if __name__ == '__main__':
    arguments = arguments()

    program = parse_file(arguments.filename)
    labels = program.labels()
    bytecode = program.bytecode()

    start_pos = int(arguments.start_position, 16)

    bytecode = Linker(start_pos).parse(labels, bytecode)

    print_output(
        labels,
        bytecode,
        start_pos,
        bytes_per_line=int(arguments.bytes_per_line)
    )
