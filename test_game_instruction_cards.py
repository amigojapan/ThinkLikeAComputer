"""Regression checks for the game-to-instruction conversion."""
import ast
from html import unescape
from pathlib import Path
import re
import unittest

from game_instruction_cards import Cards, game_cards

ROOT = Path(__file__).resolve().parent


def text(source):
    html, _ = game_cards(source, 'example', 'en')
    return unescape(re.sub('<[^>]*>', ' ', html))


class GameInstructionCards(unittest.TestCase):
    def test_every_game_statement_and_function_is_present_in_each_language(self):
        for path in ROOT.glob('*rulebook.py'):
            for lang in ('en', 'es', 'ja'):
                with self.subTest(game=path.name, lang=lang):
                    cards = Cards(path.read_text(), path.stem, lang)
                    html, count = cards.render()
                    statements = [n for n in ast.walk(cards.tree) if isinstance(n, ast.stmt)]
                    functions = [n for n in statements if isinstance(n, ast.FunctionDef)]
                    self.assertEqual(len(re.findall('data-source-line=', html)), len(statements))
                    self.assertEqual(html.count('instruction-number'), count)
                    self.assertEqual(html.count('class="instruction-card function"'), len(functions))
                    self.assertNotIn('TLAC.globals', html)

    def test_snake_slices_preserve_head_and_tail_exclusions(self):
        result = text('body = globals.snake_body[1:]\nbody = globals.snake_body[:-1]\nbody = globals.snake_body[:]')
        self.assertIn('except the first item', result)
        self.assertIn('except the last item', result)
        self.assertIn('a copy of snake body', result)

    def test_loop_exits_and_function_return_remain_distinct(self):
        result = text('while True:\n    if done:\n        break\n    continue\ndef check_win(globals):\n    return False')
        self.assertIn('Leave the innermost loop', result)
        self.assertIn('Skip to the next turn', result)
        self.assertIn('Return to the caller with result: no', result)

    def test_pacman_unused_minimum_does_not_become_a_tracker_assignment(self):
        result = text('best_move = random.choice(valid_moves)\nmin(valid_moves, key=lambda m: abs(m[1]-globals.turtle.X))')
        self.assertIn('Set chosen move to a randomly chosen item', result)
        self.assertIn('leave the stored values unchanged', result)
        self.assertEqual(result.count('Set chosen move'), 1)

    def test_flag_toggle_and_recursive_call_are_explicit(self):
        result = text('slot.flagged = not slot.flagged\nreveal_cell(globals, x + dx, y + dy)')
        self.assertIn('Set has a flag of current cell to not', result)
        self.assertIn('Call “Reveal a cell” with', result)

    def test_output_text_is_escaped_without_losing_its_content(self):
        result = text('print("<script>& hello")')
        self.assertIn('Display “<script>& hello”', result)

    def test_unsupported_syntax_fails_instead_of_dropping_a_statement(self):
        with self.assertRaises(ValueError):
            game_cards('with open("x") as file:\n    print(file)', 'example', 'en')


if __name__ == '__main__':
    unittest.main()
