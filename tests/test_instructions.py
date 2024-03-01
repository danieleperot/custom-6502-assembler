from test_compiler import ProgramTestCase


class InstructionTestCase():
    class ImpliedAddressing(ProgramTestCase):
        operand: str = ''
        bytecode: int = 0x00

        def test_does_not_expect_parameter(self):
            self._expect_error_message(
                lambda: self.program.next_instruction(f'{self.operand} $01'),
                f'[{self.operand}] ' +
                'A parameter was provided, but was not expected'
            )

        def test_is_resolved_without_parameter(self):
            self.program.next_instruction(self.operand)

            self._expect_bytecode([self.bytecode])

    class _WithAddressing(ProgramTestCase):
        operand: str = ''

        def test_requires_parameter(self):
            self._expect_error_message(
                lambda: self.program.next_instruction(self.operand),
                f'[{self.operand}] Invalid or unsupported addressing mode'
            )

    class AbsoluteAddressing(_WithAddressing):
        absolute_bytecode: int = 0x00

        def test_is_resolved_with_absolute_label(self):
            self.program.next_instruction(f'{self.operand} TO_LABEL')

            self._expect_bytecode([
                self.absolute_bytecode,
                'ABS|TO_LABEL',
                None
            ])

        def test_is_resolved_with_absolute_addressing(self):
            self.program.next_instruction(f'{self.operand} $45AB')

            self._expect_bytecode([self.absolute_bytecode, 0xAB, 0x45])

    class ImmediateAddressing(_WithAddressing):
        immediate_bytecode: int = 0x00

        def test_is_resolved_with_immediate_addressing(self):
            self.program.next_instruction(f'{self.operand} #$08')

            self._expect_bytecode([self.immediate_bytecode, 0x08])

    class ZeroPageAddressing(_WithAddressing):
        zeropage_bytecode: int = 0x00

        def test_is_resolved_with_immediate_addressing(self):
            self.program.next_instruction(f'{self.operand} $05')

            self._expect_bytecode([self.zeropage_bytecode, 0x05])


class TestInstruction_BEQ(ProgramTestCase):
    def test_requires_parameter(self):
        self._expect_error_message(
            lambda: self.program.next_instruction('BEQ'),
            '[BEQ] Only labels allowed'
        )

    def test_is_parsed_with_relative_label(self):
        self.program.next_instruction('BEQ TO_THE_LABEL')

        self._expect_bytecode([0xF0, 'REL|TO_THE_LABEL'])


class TestInstruction_CMP(InstructionTestCase.ImmediateAddressing):
    operand = 'CMP'
    immediate_bytecode = 0xC9


class TestInstruction_DEX(InstructionTestCase.ImpliedAddressing):
    operand = 'DEX'
    bytecode = 0xCA


class TestInstruction_JMP(InstructionTestCase.AbsoluteAddressing):
    operand = 'JMP'
    absolute_bytecode = 0x4C


class TestInstruction_JSR(InstructionTestCase.AbsoluteAddressing):
    operand = 'JSR'
    absolute_bytecode = 0x20


class TestInstruction_LDX(InstructionTestCase.ImmediateAddressing):
    operand = 'LDX'
    immediate_bytecode = 0xA2


class TestInstruction_NOP(InstructionTestCase.ImpliedAddressing):
    operand = 'NOP'
    bytecode = 0xEA


class TestInstruction_PHA(InstructionTestCase.ImpliedAddressing):
    operand = 'PHA'
    bytecode = 0x48


class TestInstruction_RTS(InstructionTestCase.ImpliedAddressing):
    operand = 'RTS'
    bytecode = 0x60


class TestInstruction_STA(InstructionTestCase.ZeroPageAddressing):
    operand = 'STA'
    zeropage_bytecode = 0x85


class TestInstruction_STX(InstructionTestCase.AbsoluteAddressing):
    operand = 'STX'
    absolute_bytecode = 0x8E


class TestInstruction_TSX(InstructionTestCase.ImpliedAddressing):
    operand = 'TSX'
    bytecode = 0xBA
