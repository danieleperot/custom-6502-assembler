def _labels(labels, start_pos):
    output = 'Labels:\n'
    for label, position in labels.items():
        position_hex = '{:04X}'.format(position + start_pos)
        output += f"\t0x{position_hex}: {label}"

    return output


def _instructions(bytecode, start_pos, bytes_per_line):
    output = '\nInstructions:'
    counter = 0
    for bytes_list, instruction in bytecode:
        if bytes_per_line == 1:
            output += f"\n  {instruction}"

        for byte in bytes_list:
            if counter % bytes_per_line == 0:
                output += "\n\t{:04X}: ".format(counter + start_pos)
            if isinstance(byte, str):
                output += f"{byte} "
            else:
                output += '{:02X} '.format(byte)

            counter += 1

    return output + f"\n\n\tTotal bytes: {counter}\n"


def _basic_compiler(start_pos):
    output = '\n'
    output += "\t3000 DATA -1\n"
    output += f"\t3010 PC={int(start_pos)}\n"
    output += "\t3020 X=0\n"
    output += "\t3030 READ A:IF A=-1 THEN END\n"
    output += "\t3040 POKE PC+X,A:X=X+1:GOTO 3030\n"
    output += f"\n\tSYS {int(start_pos)}"

    return output


def _basic_output(bytecode, start_pos):
    output = 'BASIC instructions:\n'
    for position, (bytes_list, instruction) in enumerate(bytecode):
        line = f"\t{(position + 1) * 10} DATA "
        line += ','.join([str(i) for i in bytes_list])

        line = line.ljust(22, " ")
        line += f":REM {instruction}\n"

        output += line

    return output + _basic_compiler(start_pos)


def print_output(labels, bytecode, start_pos, bytes_per_line=8):
    print(_labels(labels, start_pos))
    print(_instructions(bytecode, start_pos, bytes_per_line))
    print(_basic_output(bytecode, start_pos))
