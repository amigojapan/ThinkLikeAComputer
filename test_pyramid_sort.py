"""Check pyramid replay completeness and its correspondence to TLAC cards."""
import ast
import re
import unittest

import TLACsimulator as TLAC
from build_pyramid_sort import SOURCE, instruction_cards, record


class PyramidReplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.charts, cls.instructions, cls.source_map = instruction_cards()
        cls.previous_board = TLAC.globals
        cls.replay = record(cls.instructions, cls.source_map)

    def test_start_and_finish_have_the_expected_board(self):
        start = next(s for s in self.replay['steps'] if s['action'] == 'readBoardFromFile')
        self.assertEqual(start['cells'][25:30], '54312')
        final = self.replay['steps'][-1]
        self.assertEqual(final['cells'][40:45], '12345')
        self.assertEqual(final['cells'][20:30], ' ' * 10)
        self.assertEqual(final['cells'][0], ' ')
        self.assertEqual(final['event'], 'finish')
        self.assertIs(TLAC.globals, self.previous_board)

    def test_all_five_pyramids_survive_every_recorded_move(self):
        moves = [s for s in self.replay['steps'] if s['action'] == 'simulateUserInputTeleportPyramidTo']
        # Nine inversions require three temporary-space moves apiece, plus
        # five insertions into the sorting row.
        self.assertEqual(len(moves), 32)
        self.assertTrue(any(p['x'] == p['y'] == 0 for s in moves for p in s['pyramids']))
        for step in moves:
            self.assertEqual(sorted(p['size'] for p in step['pyramids']), [1, 2, 3, 4, 5])
            self.assertEqual(len({(p['x'], p['y']) for p in step['pyramids']}), 5)

    def test_sorted_prefix_is_ordered_after_every_insertion(self):
        tree = ast.parse(SOURCE.read_text())
        loop = next(n for n in tree.body if isinstance(n, ast.For))
        number = self.source_map[loop.lineno]
        lengths = []
        for step in self.replay['steps']:
            if step['line'] == number and step['event'] == 'before':
                row = next(v['value'] for v in step['variables'] if v['name'] == 'sorted_row')
                values = [v for v in row if v is not None]
                self.assertEqual(values, sorted(values))
                lengths.append(len(values))
        self.assertEqual(lengths, [0, 1, 2, 3, 4, 5])

    def test_cards_and_replay_share_numbers_in_all_languages(self):
        for lang, chart in self.charts.items():
            self.assertEqual(chart.count('instruction-number'), len(self.instructions))
            self.assertEqual([int(n) for n in re.findall(r'data-line="(\d+)"', chart)],
                             [item['number'] for item in self.instructions])
            self.assertIn('background-color: #DDA0DD; display: inline-block', chart)
            self.assertIn('background-color: #808080; display: inline-block', chart)
        for step in self.replay['steps']:
            self.assertIn(step['line'], range(len(self.instructions) + 1))
            self.assertEqual(set(step['label']), {'en', 'es', 'ja'})
            if step['event'] == 'before':
                for lang in ('en', 'es', 'ja'):
                    self.assertIn(self.instructions[step['line'] - 1]['label'][lang], step['label'][lang])
        self.assertTrue(any(s['event'] == 'call' for s in self.replay['steps']))
        self.assertTrue(any(s['event'] == 'return' for s in self.replay['steps']))

    def test_watched_values_are_saved_per_step(self):
        initial = self.replay['steps'][0]['variables']
        final = self.replay['steps'][-1]['variables']
        self.assertEqual(next(v['value'] for v in initial if v['name'] == 'sorted_row'), [None] * 10)
        self.assertEqual(next(v['value'] for v in final if v['name'] == 'sorted_row'), [1, 2, 3, 4, 5] + [None] * 5)
        self.assertIn('Final sorted board:', self.replay['steps'][-1]['output']['en'])


if __name__ == '__main__':
    unittest.main()
