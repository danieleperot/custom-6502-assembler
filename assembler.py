import sys


class AddressResolver():
    _parameters: str
    _type: str
    _value: list

    def __init__(self, parameters: str):
        self._parameters = parameters
        self._value = []
        self._type = ''
        modes = [
            self._as_immediate,
            self._as_absolute,
            self._as_label,
        ]

        for mode in modes:
            resolved = mode()
            if (resolved):
                break

    def value(self) -> list:
        return self._value

    def is_absolute(self) -> bool:
        return self._type == 'absolute' and len(self._value) == 2

    def is_zero_page(self) -> bool:
        return self._type == 'absolute' and len(self._value) == 1

    def is_immediate(self) -> bool:
        return self._type == 'immediate'

    def is_label(self) -> bool:
        return self._type == 'label'

    def is_missing(self):
        return len(self._value) == 0 and len(self._type) == 0

    def relative_label(self) -> str:
        return 'REL|' + self._value[0]

    def absolute_label(self) -> str:
        return 'ABS|' + self._value[0]

    def _as_absolute(self):
        if len(self._parameters) == 0 or self._parameters[0] != "$":
            return False

        self._assert(len(self._parameters) <= 5, 'Bad parameter length')

        self._type = 'absolute'
        high_byte = self._parameters[1:3]

        if len(self._parameters) == 3:
            self._value = [int(high_byte, 16)]
            return True

        low_byte = self._parameters[3:]
        self._value = [int(low_byte, 16), int(high_byte, 16)]

        return True

    def _as_immediate(self):
        if len(self._parameters) == 0 or self._parameters[0] != "#":
            return False

        self._assert(len(self._parameters) <= 4, 'Bad parameter length')

        self._assert(self._parameters[1] == '$', 'Only hex values supported')

        self._type = 'immediate'
        self._value = [int(self._parameters[2:], 16)]

        return True

    def _as_label(self):
        if len(self._parameters) == 0:
            return False

        self._type = 'label'
        self._value = [self._parameters]

        return True

    def _assert(self, condition, message):
        assert condition, f'Line {LINE_NUMBER}: {message}'


def op_beq(address: AddressResolver):
    # Only relative addresses (displacements) allowed
    if address.is_label():
        return [0xF0, address.relative_label()]

    assert False, f'Line {LINE_NUMBER}: Only labels allowed'


def op_cmp(address: AddressResolver):
    # Immediate    CMP #$44     $C9
    # Zero Page    CMP $44      $C5
    # Zero Page,X  CMP $44,X    $D5
    # Absolute     CMP $4400    $CD
    # Absolute,X   CMP $4400,X  $DD
    # Absolute,Y   CMP $4400,Y  $D9
    # (Indirect,X) CMP ($44,X)  $C1
    # (Indirect),Y CMP ($44),Y  $D1

    if address.is_immediate():
        return [0xC9, *address.value()]

    assert False, f'Line {LINE_NUMBER}: unknown addressing mode'


def op_dex(address: AddressResolver):
    if address.is_missing():
        return [0xCA]

    assert False, f'Line {LINE_NUMBER}: parameter provided but not expected'


def op_jmp(address: AddressResolver):
    # Absolute JMP $5597   $4C
    # Indirect JMP ($5597) $6C
    if address.is_absolute():
        return [0x4C, *address.value()]

    if address.is_label():
        return [0x4C, address.absolute_label()]

    assert False, f'Line {LINE_NUMBER}: unknown addressing mode'


def op_jsr(address: AddressResolver):
    # Only absolute mode is supported
    if address.is_absolute():
        return [0x20, *address.value()]

    assert address is not None, f'Line {LINE_NUMBER}: address is invalid'


def op_pha(address: AddressResolver):
    if address.is_missing():
        return [0x48]

    assert False, f'Line {LINE_NUMBER}: parameter provided but not expected'


def op_rts(address: AddressResolver):
    if address.is_missing():
        return [0x60]

    assert False, f'Line {LINE_NUMBER}: parameter provided but not expected'


def op_sta(address: AddressResolver):
    # Zero Page    STA $44      $85
    # Zero Page,X  STA $44,X    $95
    # Absolute     STA $4400    $8D
    # Absolute,X   STA $4400,X  $9D
    # Absolute,Y   STA $4400,Y  $99
    # (Indirect,X) STA ($44,X)  $81
    # (Indirect),Y STA ($44),Y  $91

    if address.is_zero_page():
        return [0x85, *address.value()]

    assert False, f'Line {LINE_NUMBER}: unknown addressing mode'


def op_stx(address: AddressResolver):
    # Zero Page   STX $44   $86
    # Zero Page,Y STX $44,Y $96
    # Absolute    STX $4400 $8E

    if address.is_absolute():
        return [0x8E, *address.value()]

    assert False, f'Line {LINE_NUMBER}: unknown addressing mode'


def op_tsx(address: AddressResolver):
    if address.is_missing():
        return [0xBA]

    assert False, f'Line {LINE_NUMBER}: parameter provided but not expected'


def parse_line(instruction):
    operation = instruction[0:3]
    parameters = instruction[3:].strip()
    parser = ALL_INSTRUCTIONS.get(operation)
    assert parser, f'Line {LINE_NUMBER}: Unknown instruction "{operation}"'

    address = AddressResolver(parameters)

    return parser(address)


def parse_file(file):
    global LINE_NUMBER

    program_counter = 0
    labels = {}
    bytecode = []

    with open(file, "r") as source:
        line = source.readline()

        while line:
            LINE_NUMBER += 1
            comment_position = line.find(';')
            instruction = line[:comment_position].strip()
            if instruction:
                print(f"Parsing line {LINE_NUMBER}: {instruction}")
                if instruction.endswith(':'):
                    labels[instruction[:-1]] = program_counter
                else:
                    parsed = parse_line(instruction)
                    program_counter += len(parsed)
                    bytecode.append([parsed, instruction])

            line = source.readline()

    return (labels, bytecode)


# ==== GLOBALS ==== #
ALL_INSTRUCTIONS = {
    'BEQ': op_beq,
    'CMP': op_cmp,
    'DEX': op_dex,
    'JMP': op_jmp,
    'JSR': op_jsr,
    'PHA': op_pha,
    'RTS': op_rts,
    'STA': op_sta,
    'STX': op_stx,
    'TSX': op_tsx,
}

LINE_NUMBER = 0
# ================= #


if __name__ == '__main__':
    assert len(sys.argv) > 1, "No file provided. Please provide a file path."
    labels, bytecode = parse_file(sys.argv[1])

    print('Labels:')
    for position, label in labels.items():
        print(f"\t{label}: {position}")

    print('Instructions:', end="")
    counter = 0
    for instruction in bytecode:
        for byte in instruction[0]:
            if counter % 8 == 0:
                print("\n\t{:04X}".format(counter), end=": ")
            if isinstance(byte, str):
                print(byte, end=" ")
            else:
                print('{:02X}'.format(byte), end=" ")

            counter += 1

    print()
    print('BASIC instructions: ')
    for position, instructions in enumerate(bytecode):
        line = f"\t{(position + 1) * 10} DATA "
        line += ','.join([str(i) for i in instructions[0]])

        line = line.ljust(22, " ")
        line += f":REM {instructions[1]}"

        print(line)
