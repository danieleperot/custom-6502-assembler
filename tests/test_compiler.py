import unittest

from src.compiler import Program


class ProgramTestCase(unittest.TestCase):
    program: Program

    def setUp(self):
        self.program = Program()

    def _expect_bytecode(self, expected: list[int | str | None]):
        self.assertEqual(expected, self.program.bytecode()[0][0])

    def _expect_full_bytecode(self, expected: list[int | str]):
        bytecode = []
        for (bytes_list, _) in self.program.bytecode():
            bytecode.extend(bytes_list)

        self.assertEqual(expected, bytecode)

    def _expect_error_message(self, statement, expected: str):
        try:
            statement()
            self.assertFalse(True, 'An assertion was supposed to fail!')
        except AssertionError as error:
            self.assertEqual(f"[ERROR] Line 1: {expected}", str(error))


class TestCompilerGrammar(ProgramTestCase):
    def test_empty_lines_are_ignored(self):
        self.program.next_instruction("")

        self.assertEqual([], self.program.bytecode())

    def test_lines_starting_with_comment_are_ignored(self):
        self.program.next_instruction("; This is a comment")

        self.assertEqual([], self.program.bytecode())

    def test_empty_lines_with_comment_are_ignored(self):
        self.program.next_instruction("  ; test test  ")

        self.assertEqual([], self.program.bytecode())

    def test_instruction_is_parsed(self):
        self.program.next_instruction('NOP')

        self._expect_bytecode([0xEA])

    def test_instruction_is_parsed_even_if_surrounded_by_whitespaces(self):
        self.program.next_instruction('     NOP      ')

        self._expect_bytecode([0xEA])

    def test_comment_is_ignored_when_is_inlined_to_instruction(self):
        self.program.next_instruction('NOP ; a very cool comment!')

        self._expect_bytecode([0xEA])

    def test_comment_is_ignored_when_inline_and_instruction_whitespaced(self):
        self.program.next_instruction('    NOP; another comment?')

        self._expect_bytecode([0xEA])

    def test_parse_instruction_with_immediate_addressing(self):
        self.program.next_instruction('LDX #$5B')

        self._expect_bytecode([0xA2, 0x5B])

    def test_parse_instruction_with_absolute_addressing(self):
        self.program.next_instruction('JMP $38AD')

        self._expect_bytecode([0x4C, 0xAD, 0x38])

    def test_label_is_recognized_if_it_ends_with_colon(self):
        self.program.next_instruction('TEST:')

        self.assertEqual(['TEST'], list(self.program.labels().keys()))

    def test_label_is_recognized_when_whitespaced(self):
        self.program.next_instruction('   TEST:  ')

        self.assertEqual(['TEST'], list(self.program.labels().keys()))

    def test_label_content_is_stripped(self):
        self.program.next_instruction('  TEST   : ')

        self.assertEqual(['TEST'], list(self.program.labels().keys()))


class TestCompilerMultiLineProgram(ProgramTestCase):
    def test_program_with_only_comments_is_empty(self):
        self.program.next_instruction('')
        self.program.next_instruction('; test')
        self.program.next_instruction('   ;   hello')

        self.assertEqual([], self.program.bytecode())

    def test_multiple_instructions_are_loaded(self):
        self.program.next_instruction('NOP')
        self.program.next_instruction('NOP')

        self._expect_full_bytecode([0xEA, 0xEA])

    def test_label_at_beginning_of_program_has_address_zero(self):
        self.program.next_instruction('START:')
        self.program.next_instruction('  NOP')

        self.assertEqual(0, self.program.labels()['START'])

    def test_multiple_labels_at_beginning_have_address_zero(self):
        self.program.next_instruction('FIRST:')
        self.program.next_instruction('SECOND:')
        self.program.next_instruction('  NOP')

        self.assertEqual(0, self.program.labels()['FIRST'])
        self.assertEqual(0, self.program.labels()['SECOND'])

    def test_label_after_instruction_has_address_right_position_address(self):
        self.program.next_instruction('FIRST:')
        self.program.next_instruction('NOP')  # 1 byte
        self.program.next_instruction('NOP')  # 1 byte
        self.program.next_instruction('SECOND:')
        self.program.next_instruction('THIRD:')
        self.program.next_instruction('NOP')  # 1 byte
        self.program.next_instruction('END:')

        self.assertEqual(0, self.program.labels()['FIRST'])
        self.assertEqual(2, self.program.labels()['SECOND'])
        self.assertEqual(2, self.program.labels()['THIRD'])
        self.assertEqual(3, self.program.labels()['END'])
