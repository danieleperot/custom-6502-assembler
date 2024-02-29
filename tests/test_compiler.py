import unittest

from src.compiler import Program


class TestCompilerGrammar(unittest.TestCase):
    def test_empty_lines_are_ignored(self):
        program = Program()
        program.next_instruction("")

        self.assertEqual([], program.bytecode())

    def test_lines_starting_with_comment_are_ignored(self):
        program = Program()
        program.next_instruction("; This is a comment")

        self.assertEqual([], program.bytecode())

    def test_empty_lines_with_comment_are_ignored(self):
        program = Program()
        program.next_instruction("  ; test test  ")

        self.assertEqual([], program.bytecode())


class TestCompilerInstructions(unittest.TestCase):
    def test_dex(self):
        program = Program()
        program.next_instruction('  DEX  ')

        self.assertEqual([0xCA], program.bytecode()[0][0])
