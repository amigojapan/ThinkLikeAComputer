"""Verify the basics debugger's actual recorded state and output."""
import unittest

from build_TLAC_basics_executions import EXAMPLES, SOURCES, record


def variable(step, name, scope='global'):
    return next(value['value'] for value in step['variables']
                if value['name'] == name and value['scope'] == scope)


class BasicsExecutions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runs = {key: record(key) for key in SOURCES}

    def test_instruction_numbers_and_translations_match_the_lesson(self):
        for key, run in self.runs.items():
            with self.subTest(example=key):
                self.assertEqual(len(SOURCES[key].splitlines()), len(EXAMPLES['charts'][key]))
                for step in run['steps']:
                    self.assertIn(step['line'], range(len(run['instructions']) + 1))
                    self.assertEqual(set(step['label']), {'en', 'es', 'ja'})
                    self.assertEqual(set(step['output']), {'en', 'es', 'ja'})
                self.assertTrue(run['tutorial'].endswith('8_basics_of_programming_TLAC.html'))

    def test_turtle_final_positions_and_square_eggs(self):
        positions = {'functions': (9, 9), 'input': (0, 0), 'for': (9, 9),
                     'countdown': (4, 3), 'do-while': (4, 3), 'foreach': (6, 5)}
        for key, (x, y) in positions.items():
            with self.subTest(example=key):
                turtle = self.runs[key]['steps'][-1]['turtles'][0]
                self.assertEqual((turtle['x'], turtle['y'], turtle['direction']), (x, y, '^'))
        self.assertEqual(self.runs['functions']['steps'][-1]['eggs'], [80, 81, 85, 86, 88, 89, 90, 91, 95, 96, 98, 99])

    def test_saved_player_position_and_counter_values(self):
        final = self.runs['input']['steps'][-1]
        self.assertEqual(variable(final, 'savedX'), 0)
        self.assertEqual(variable(final, 'savedY'), 0)
        final = self.runs['do-while']['steps'][-1]
        self.assertEqual(variable(final, 'n1'), 4)
        self.assertEqual(final['output']['en'].splitlines(), [
            'The value of n1 is 1', 'The value of n1 is 2',
            'The value of n1 is 3', 'n1 has passed the limit'])
        self.assertIn('El valor de n1 es 2', final['output']['es'])
        self.assertIn('n1の値は 2', final['output']['ja'])

    def test_text_output_preserves_multiplications_and_pyramid_spacing(self):
        nested = self.runs['nested']['steps'][-1]['output']['en']
        rows = [row for row in nested.splitlines() if row.strip()]
        self.assertEqual(len(rows), 3)
        for i, row in enumerate(rows, 1):
            self.assertEqual(row, ''.join(f'    {i} * {j} = {i*j}' for j in range(1, 4)))
        pyramid = self.runs['pyramid']['steps'][-1]['output']['en']
        self.assertEqual(pyramid, '     *\n    ***\n   *****\n  *******\n *********\n')
        self.assertFalse(self.runs['nested']['has_board'])
        self.assertFalse(self.runs['pyramid']['has_board'])

    def test_list_snapshots_are_not_mutated_by_later_steps(self):
        steps = self.runs['lists']['steps']
        first_list = next(s for s in steps if any(v['name'] == 'fruits' for v in s['variables']))
        self.assertEqual(variable(first_list, 'fruits'), ['banana', 'apple', 'peach', 'pear'])
        self.assertEqual(variable(steps[-1], 'fruits'), ['apple', 'banana', 'blueberry', 'pear', 'appricot'])
        self.assertEqual(steps[0]['output']['en'], '')
        self.assertEqual(steps[-1]['output']['en'].splitlines()[-5:], ['apple', 'banana', 'blueberry', 'pear', 'appricot'])

    def test_function_parameters_are_visible_in_the_current_frame(self):
        body = next(s for s in self.runs['pyramid']['steps']
                    if s['depth'] == 1 and s['line'] == 5)
        self.assertEqual(variable(body, 'ch', 'local'), '*')
        self.assertEqual(variable(body, 'times', 'local'), 1)
        self.assertEqual(variable(body, 'triangle_width', 'local'), 5)
        self.assertEqual(variable(body, 'i'), 1)


if __name__ == '__main__':
    unittest.main()
