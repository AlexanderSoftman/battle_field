from PyQt5 import QtCore
import unittest
import logging
import math

from battle_field.common.bump_checker import bump_checker_new
from battle_field.common import functions

LOG = logging.getLogger(__name__)
LOG.critical("TestBumpCheckerNew start")


# measure
class BumpCheckerNewTestCase(unittest.TestCase):
    rounding_error = 0.001
    bump_checker_new_m = bump_checker_new.BumpCheckerNew()
    small_rect_half_sides = {
        "x": 50,
        "y": 50,
    }
    big_rect_half_sides = {
        "x": 100,
        "y": 100,
    }
    small_rect = QtCore.QRectF(
        - small_rect_half_sides["x"],
        - small_rect_half_sides["y"],
        2 * small_rect_half_sides["x"],
        2 * small_rect_half_sides["y"])
    big_rect = QtCore.QRectF(
        - big_rect_half_sides["x"],
        - big_rect_half_sides["y"],
        2 * big_rect_half_sides["x"],
        2 * big_rect_half_sides["y"])

    def test_moving_line(self):
        asker_lines = [
            QtCore.QLineF(
                QtCore.QPointF(-50, -50),
                QtCore.QPointF(-50, 50)),
            QtCore.QLineF(
                QtCore.QPointF(-50, 50),
                QtCore.QPointF(50, 50)),
            QtCore.QLineF(
                QtCore.QPointF(50, 50),
                QtCore.QPointF(50, - 50)),
            QtCore.QLineF(
                QtCore.QPointF(50, -50),
                QtCore.QPointF(-50, -50))]
        # only one dot "inside" line
        item_line_one_dot = QtCore.QLineF(
            QtCore.QPointF(100, 100),
            QtCore.QPointF(-100, -100))
        moving_line = self.bump_checker_new_m.moving_line(
            asker_lines, item_line_one_dot)
        self.assertAlmostEqual(moving_line.p1().x(), -50)
        self.assertAlmostEqual(moving_line.p1().y(), 50)
        self.assertAlmostEqual(moving_line.p2().x(), 0)
        self.assertAlmostEqual(moving_line.p2().y(), 0)
        # two dots "inside" line simmetric
        item_line_two_dots = QtCore.QLineF(
            QtCore.QPointF(-30, 100),
            QtCore.QPointF(-30, -100))
        moving_line = self.bump_checker_new_m.moving_line(
            asker_lines, item_line_two_dots)
        self.assertAlmostEqual(moving_line.p1().x(), -50)
        self.assertAlmostEqual(moving_line.p2().x(), -30)
        self.assertAlmostEqual(moving_line.p1().y(), moving_line.p2().y())
        # all dots "inside" line
        item_line_all_dots = QtCore.QLineF(
            QtCore.QPointF(100, 100),
            QtCore.QPointF(100, -100))
        moving_line = self.bump_checker_new_m.moving_line(
            asker_lines, item_line_all_dots)
        self.assertAlmostEqual(moving_line.p1().x(), -50)
        self.assertAlmostEqual(moving_line.p2().x(), 100)
        self.assertAlmostEqual(moving_line.p1().y(), moving_line.p2().y())
        # no dots "inside" line
        item_line_all_dots = QtCore.QLineF(
            QtCore.QPointF(-100, 100),
            QtCore.QPointF(-100, -100))
        moving_line = self.bump_checker_new_m.moving_line(
            asker_lines, item_line_all_dots)
        self.assertTrue(moving_line is None)
        # two dots "inside" line NOT simmetric
        item_line_two_dots_not_simmetric = QtCore.QLineF(
            QtCore.QPointF(40, 50),
            QtCore.QPointF(-40, -50))
        moving_line = self.bump_checker_new_m.moving_line(
            asker_lines, item_line_two_dots_not_simmetric)
        self.assertAlmostEqual(moving_line.p1().x(), -50)
        self.assertAlmostEqual(moving_line.p1().y(), 50)
        self.assertAlmostEqual(moving_line.p2().x(), 4.87804878)
        self.assertAlmostEqual(moving_line.p2().y(), 6.09756097)
        # two dots inside line NOT simmetric with half file
        item_line_two_dots_not_simmetric = QtCore.QLineF(
            QtCore.QPointF(40, 50),
            QtCore.QPointF(0, 0))
        moving_line = self.bump_checker_new_m.moving_line(
            asker_lines, item_line_two_dots_not_simmetric)
        self.assertAlmostEqual(moving_line.p1().x(), -50)
        self.assertAlmostEqual(moving_line.p1().y(), 50)
        self.assertAlmostEqual(moving_line.p2().x(), 4.87804878)
        self.assertAlmostEqual(moving_line.p2().y(), 6.09756097)
        # two dots inside line NOT simmetric with half file
        item_line_two_dots_not_simmetric = QtCore.QLineF(
            QtCore.QPointF(0, 0),
            QtCore.QPointF(-40, -50))
        moving_line = self.bump_checker_new_m.moving_line(
            asker_lines, item_line_two_dots_not_simmetric)
        self.assertAlmostEqual(moving_line.p1().x(), -50)
        self.assertAlmostEqual(moving_line.p1().y(), 40)
        self.assertAlmostEqual(moving_line.p2().x(), 0)
        self.assertAlmostEqual(moving_line.p2().y(), 0)
        # three dots inside line
        item_line_two_dots_not_simmetric = QtCore.QLineF(
            QtCore.QPointF(50, -45),
            QtCore.QPointF(45, -50))
        moving_line = self.bump_checker_new_m.moving_line(
            asker_lines, item_line_two_dots_not_simmetric)
        self.assertAlmostEqual(moving_line.p1().x(), -50)
        self.assertAlmostEqual(moving_line.p1().y(), 50)
        self.assertAlmostEqual(moving_line.p2().x(), 47.5)
        self.assertAlmostEqual(moving_line.p2().y(), -47.5)


if __name__ == '__main__':
    unittest.main()
