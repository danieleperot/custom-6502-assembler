import sys

from compiler import Program
from linker import Linker


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

    print('Labels:')
    for position, label in labels.items():
        print(f"\t{label}: {position}")

    print('Instructions:', end="")
    counter = 0
    for bytes_list, instruction in bytecode:
        for byte in bytes_list:
            if counter % 8 == 0:
                print("\n\t{:04X}".format(counter + start_pos), end=": ")
            if isinstance(byte, str):
                print(byte, end=" ")
            else:
                print('{:02X}'.format(byte), end=" ")

            counter += 1

    print()
    print('BASIC instructions: ')
    for position, (bytes_list, instruction) in enumerate(bytecode):
        line = f"\t{(position + 1) * 10} DATA "
        line += ','.join([str(i) for i in bytes_list])

        line = line.ljust(22, " ")
        line += f":REM {instruction}"

        print(line)
