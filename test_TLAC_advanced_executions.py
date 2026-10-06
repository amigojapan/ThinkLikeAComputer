"""Check recorded execution against the original runnable TLAC programs."""
import contextlib
import io
import runpy
import sys
import unittest
from pathlib import Path

import TLACsimulator as TLAC
from build_TLAC_advanced_executions import record

ROOT = Path(__file__).resolve().parent


def state():
    board = TLAC.globals
    turtles = getattr(board, 'lesson_turtles', [board.turtle])
    return {
        'eggs': [i for i, cell in enumerate(board.slots) if cell.containsEgg],
        'turtles': [{'name': getattr(turtle, 'name', 'Turtle'), 'x': turtle.X,
                     'y': turtle.Y, 'direction': turtle.direction} for turtle in turtles],
    }


def run_original(filename):
    board = TLAC.initGlobals()
    board.W = board.H = 10
    board.slots = TLAC.initSlots(board)
    board.turtle = TLAC.initTurtle()
    board.ghosts = []
    TLAC.globals = board
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            runpy.run_path(str(ROOT / filename), run_name='__main__')
        except SystemExit as result:
            if result.code not in (None, 0):
                raise
    return state()


class Executions(unittest.TestCase):
    def test_all_problem_runs_match_original_scripts(self):
        expected_eggs = {4: 36, 5: 16, 6: 100, 7: 50, 8: 25}
        for n in range(4, 9):
            finals = []
            for kind, suffix in [('loop', '-non-recursive'), ('recursive', '')]:
                with self.subTest(problem=n, kind=kind):
                    original = run_original(f'problem{n}-program{suffix}.py')
                    trace = record(f'problem{n}-{kind}')
                    final = trace['steps'][-1]
                    self.assertEqual(final['eggs'], original['eggs'])
                    self.assertEqual(final['turtles'], original['turtles'])
                    self.assertEqual(len(final['eggs']), expected_eggs[n])
                    self.assertTrue(all(set(step['label']) == {'en', 'es', 'ja'} for step in trace['steps']))
                    self.assertTrue(all(len(step['cells']) == trace['width'] * trace['height'] for step in trace['steps']))
                    finals.append((final['cells'], final['eggs'], final['turtles']))
            self.assertEqual(*finals, f'Loop/recursive final boards differ for {n}')

    def test_recursion_records_calls_returns_and_stopping(self):
        trace = record('problem6-recursive')['steps']
        self.assertTrue(any('Enter function' in s['label']['en'] for s in trace))
        self.assertTrue(any('Return from function' in s['label']['en'] for s in trace))
        self.assertGreater(max(s['depth'] for s in trace), 2)
        self.assertEqual(trace[-2]['label']['en'], 'End Program')
        self.assertEqual(trace[-1]['label']['en'], 'Finished: final board')

    def test_class_runs_match_executable_examples(self):
        for key, source in [('classes-turtle', 'docs_classes_turtle.py'),
                            ('classes-two-turtles', 'docs_classes_two_turtles.py')]:
            with self.subTest(example=key):
                original = run_original(source)
                final = record(key)['steps'][-1]
                self.assertEqual(final['turtles'], original['turtles'])
                self.assertEqual(final['eggs'], original['eggs'])

    def test_turtle_objects_keep_independent_state(self):
        trace = record('classes-two-turtles')['steps']
        self.assertEqual(trace[-1]['turtles'], [
            {'name': 'Aki', 'x': 1, 'y': 2, 'direction': '^'},
            {'name': 'Sol', 'x': 5, 'y': 4, 'direction': '>'},
        ])
        self.assertEqual(trace[-1]['eggs'], [19, 25, 28])
        moving_sol = [s for s in trace if s['label']['en'].startswith('After: Sol:')]
        self.assertTrue(moving_sol)
        self.assertTrue(all(s['turtles'][0] == trace[-1]['turtles'][0] for s in moving_sol))
        # The new egg is retained while the turtle picture covers its square.
        laid = next(s for s in trace if s['label']['en'] == 'After: Sol: Place an egg')
        self.assertIn(28, laid['eggs'])
        self.assertEqual(laid['cells'][28], '>')

    def test_recording_restores_simulator_functions_and_tracer(self):
        original_forward, original_trace = TLAC.fd, sys.gettrace()
        record('classes-turtle')
        self.assertIs(TLAC.fd, original_forward)
        self.assertIs(sys.gettrace(), original_trace)


if __name__ == '__main__':
    unittest.main()
