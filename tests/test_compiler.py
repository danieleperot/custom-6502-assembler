import unittest

from src.compiler import Program


class ProgramTestCase(unittest.TestCase):
    program: Program

    def setUp(self):
        self.program = Program()

    def _expect_bytecode(self, expected: list[int | str]):
        self.assertEqual(expected, self.program.bytecode()[0][0])


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


class TestCompilerInstructions(unittest.TestCase):
    def test_dex(self):
        program = Program()
        program.next_instruction('DEX  ')

        self.assertEqual([0xCA], program.bytecode()[0][0])
