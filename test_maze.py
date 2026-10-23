"""Validate the recorded maze run against the source, board and TLAC cards."""
import re
import unittest

import TLACloopyLib as loops
import TLACsimulator as TLAC
from build_maze import ROOT, instruction_cards, record


class MazeReplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.charts, cls.instructions, cls.source_map = instruction_cards()
        cls.old_board, cls.old_loops = TLAC.globals, loops.globals
        cls.replay = record(cls.instructions, cls.source_map)
        cls.steps = cls.replay['steps']

    def test_start_goal_and_state_restoration(self):
        self.assertEqual(self.steps[0]['turtles'][0], dict(name='Turtle', x=4, y=9, direction='^'))
        self.assertEqual(self.steps[0]['cells'][78], 'G')
        final = self.steps[-1]
        self.assertEqual((final['turtles'][0]['x'], final['turtles'][0]['y']), (8, 7))
        self.assertEqual(final['event'], 'finish')
        self.assertTrue(final['variables'][0]['value'])
        goal_checks = [s for s in self.steps if s['action'] == 'amILayingOnTheGoalFlag']
        self.assertTrue(goal_checks[-1]['result'])
        self.assertFalse(any(s['result'] for s in goal_checks[:-1]))
        self.assertIs(TLAC.globals, self.old_board)
        self.assertIs(loops.globals, self.old_loops)

    def test_moves_are_adjacent_passable_and_preceded_by_a_successful_check(self):
        board = re.findall(r'\[(.)\]', (ROOT / 'complexMaze2.txt').read_text())
        moves = 0
        previous_action = None
        for previous, step in zip(self.steps, self.steps[1:]):
            turtle, old = step['turtles'][0], previous['turtles'][0]
            self.assertTrue(0 <= turtle['x'] < 10 and 0 <= turtle['y'] < 10)
            self.assertNotEqual(board[turtle['y'] * 10 + turtle['x']], '#')
            if step['action'] == 'fd':
                moves += 1
                self.assertEqual(abs(turtle['x'] - old['x']) + abs(turtle['y'] - old['y']), 1)
                self.assertEqual(previous_action['action'], 'testIfICanProceed')
                self.assertTrue(previous_action['result'])
            else:
                self.assertEqual((turtle['x'], turtle['y']), (old['x'], old['y']))
            if step['event'] == 'action':
                previous_action = step
        self.assertGreater(moves, 0)

    def test_left_checks_restore_the_direction_and_position(self):
        entering = None
        for step in self.steps:
            if 'Check the path on the left' not in step['label']['en']:
                continue
            if step['event'] == 'call':
                entering = step['turtles'][0]
            elif step['event'] == 'return':
                self.assertEqual(step['turtles'][0], entering)
                entering = None
        self.assertIsNone(entering)

    def test_cards_match_replay_and_images_exist(self):
        from TLAC_boardgame.execution_view import TILES
        for chart in self.charts.values():
            numbers = [int(n) for n in re.findall(r'data-line="(\d+)"', chart)]
            self.assertEqual(numbers, [item['number'] for item in self.instructions])
        for step in self.steps:
            self.assertEqual(set(step['label']), {'en', 'es', 'ja'})
            self.assertIn(step['line'], range(len(self.instructions) + 1))
            if step['event'] == 'before':
                for lang in ('en', 'es', 'ja'):
                    self.assertIn(self.instructions[step['line'] - 1]['label'][lang], step['label'][lang])
            for cell in set(step['cells']):
                self.assertTrue((ROOT / self.replay['image_root'] / TILES[cell]).is_file())


if __name__ == '__main__':
    unittest.main()
