import unittest
import logging
import random

from battle_field.slam import least_squares_method

LOG = logging.getLogger(__name__)
LOG.critical("LeastSquaresMethodTest start")


# measure
class LeastSquaresMethodTest(unittest.TestCase):

    # move line
    def test_least_squares_method(self):
        # create line y = 0 * x + 0, count of dots = 33
        list_of_dots = self.create_random_dots((0, 0), 33)
        line_restored = least_squares_method.approximate_line(list_of_dots)
        self.assertAlmostEqual(line_restored[0], 0)
        self.assertAlmostEqual(line_restored[1], 0)
        # create line y = 0 * x + 3, count of dots = 5
        list_of_dots = self.create_random_dots((0, 3), 5)
        line_restored = least_squares_method.approximate_line(list_of_dots)
        self.assertAlmostEqual(line_restored[0], 0)
        self.assertAlmostEqual(line_restored[1], 3)
        # create line y = 4 * x - 7, count of dots = 4
        list_of_dots = self.create_random_dots((4, -7), 4)
        line_restored = least_squares_method.approximate_line(list_of_dots)
        self.assertAlmostEqual(line_restored[0], 4)
        self.assertAlmostEqual(line_restored[1], -7)
        # create line y = -33 * x + 71, count of dots = 29
        list_of_dots = self.create_random_dots((-33, 71), 29)
        line_restored = least_squares_method.approximate_line(list_of_dots)
        self.assertAlmostEqual(line_restored[0], -33)
        self.assertAlmostEqual(line_restored[1], 71)
        # create line x = 3, count of dots = 9
        list_of_dots = self.create_random_dots((3,), 9)
        line_restored = least_squares_method.approximate_line(list_of_dots)
        self.assertAlmostEqual(line_restored[0], 3)
        # count of dots = 0
        self.assertTrue(least_squares_method.approximate_line([]) is None)

    # input - (k, b) if y = kx + b valid or (x) if x = 3
    def create_random_dots(self, line_options, count_of_dots):
        dot_list = []
        if len(line_options) == 1:
            for i in range(1, count_of_dots, 1):
                y = random.uniform(-1000, 1000)
                dot_list.append((line_options[0], y))
        elif len(line_options) == 2:
            for i in range(1, count_of_dots, 1):
                x = random.uniform(-1000, 1000)
                dot_list.append((x, line_options[0] * x + line_options[1]))
        else:
            # strange situation
            pass
        return dot_list


if __name__ == '__main__':
    unittest.main()
