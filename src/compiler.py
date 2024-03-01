from .address import AddressResolver


class Program:
    _labels: dict[str, bool]
    _bytecode: list[tuple[list, str]]
    _program_counter: int
    _line_number: int
    _operands: dict[str, callable]

    def __init__(self):
        self._labels = {}
        self._bytecode = []
        self._program_counter = 0
        self._line_number = 0
        self._operands = {
            'BEQ': self.op_beq,
            'CMP': self.op_cmp,
            'DEX': self.op_dex,
            'JMP': self.op_jmp,
            'JSR': self.op_jsr,
            'LDX': self.op_ldx,
            'NOP': self.op_nop,
            'PHA': self.op_pha,
            'RTS': self.op_rts,
            'STA': self.op_sta,
            'STX': self.op_stx,
            'TSX': self.op_tsx,
        }

    def labels(self) -> dict[str, bool]:
        return self._labels

    def bytecode(self) -> list[tuple[list[str | int | None], str]]:
        return self._bytecode

    def next_instruction(self, line: str):
        self._line_number += 1
        instruction = line.strip()

        comment_position = line.find(';')
        if comment_position != -1:
            instruction = line[:comment_position].strip()

        if not instruction:
            return

        if instruction.endswith(':'):
            self._labels[instruction[:-1].strip()] = self._program_counter
        else:
            parsed = self._parse_instruction(instruction)
            self._program_counter += len(parsed)
            self._bytecode.append((parsed, instruction))

    def _parse_instruction(self, instruction):
        operand = instruction[0:3]
        parameters = instruction[3:].strip()
        parser = self._operands.get(operand)
        self._assert(parser is not None, f'Unknown instruction "{operand}"')

        address = AddressResolver(parameters, self._line_number)

        return parser(address)

    def op_beq(self, address: AddressResolver):
        if address.is_label():
            return [0xF0, *address.relative_label()]

        self._error('[BEQ] Only labels allowed')

    def op_cmp(self, address: AddressResolver):
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

        self._error('[CMP] Invalid or unsupported addressing mode')

    def op_dex(self, address: AddressResolver):
        if address.is_missing():
            return [0xCA]

        self._error('[DEX] A parameter was provided, but was not expected')

    def op_jmp(self, address: AddressResolver):
        # Indirect JMP ($5597) $6C
        if absolute := self._resolve_absolute(0x4C, address):
            return absolute

        self._error('[JMP] Invalid or unsupported addressing mode')

    def op_jsr(self, address: AddressResolver):
        if absolute := self._resolve_absolute(0x20, address):
            return absolute

        self._error('[JSR] Invalid or unsupported addressing mode')

    def op_ldx(self, address: AddressResolver):
        # Immediate   LDX #$44    $A2
        # Zero Page   LDX $44     $A6
        # Zero Page,Y LDX $44,Y   $B6
        # Absolute    LDX $4400   $AE
        # Absolute,Y  LDX $4400,Y $BE
        if address.is_immediate():
            return [0xA2, *address.value()]

        self._error('[LDX] Invalid or unsupported addressing mode')

    def op_nop(self, address: AddressResolver):
        if address.is_missing():
            return [0xEA]

        self._error('[NOP] A parameter was provided, but was not expected')

    def op_pha(self, address: AddressResolver):
        if address.is_missing():
            return [0x48]

        self._error('[PHA] A parameter was provided, but was not expected')

    def op_rts(self, address: AddressResolver):
        if address.is_missing():
            return [0x60]

        self._error('[RTS] A parameter was provided, but was not expected')

    def op_sta(self, address: AddressResolver):
        # Zero Page    STA $44      $85
        # Zero Page,X  STA $44,X    $95
        # Absolute     STA $4400    $8D
        # Absolute,X   STA $4400,X  $9D
        # Absolute,Y   STA $4400,Y  $99
        # (Indirect,X) STA ($44,X)  $81
        # (Indirect),Y STA ($44),Y  $91

        if address.is_zero_page():
            return [0x85, *address.value()]

        self._error('[STA] Invalid or unsupported addressing mode')

    def op_stx(self, address: AddressResolver):
        # Zero Page   STX $44   $86
        # Zero Page,Y STX $44,Y $96

        if absolute := self._resolve_absolute(0x8E, address):
            return absolute

        self._error('[STX] Invalid or unsupported addressing mode')

    def op_tsx(self, address: AddressResolver):
        if address.is_missing():
            return [0xBA]

        self._error('[TSX] A parameter was provided, but was not expected')

    def _resolve_absolute(
        self,
        bytecode: int,
        address: AddressResolver
    ) -> list | None:
        if address.is_absolute():
            return [bytecode, *address.value()]

        if address.is_label():
            return [bytecode, *address.absolute_label()]

        return None

    def _assert(self, condition: bool, error: str):
        assert condition, f'[ERROR] Line {self._line_number}: {error}'

    def _error(self, error: str):
        self._assert(False, error)
