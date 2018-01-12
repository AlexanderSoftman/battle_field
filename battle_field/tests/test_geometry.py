from PyQt5 import QtCore
import unittest
import logging
import math

from battle_field.common import geometry

LOG = logging.getLogger(__name__)
LOG.critical("GeometryTestCase start")


# measure
class GeometryTestCase(unittest.TestCase):

    def test_intersect_by_secant(self):
        secant_line = QtCore.QLineF(
            QtCore.QPointF(1000, 0),
            QtCore.QPointF(1010, 0))
        lines = [
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
        res = geometry.intersect_by_secant(
            QtCore.QPointF(0, 0),
            secant_line,
            lines)
        self.assertTrue(len(res) == 2)

    # move line
    def test_move_line_to_new_dot(self):
        old_line = QtCore.QLineF(
            QtCore.QPointF(0, 0),
            QtCore.QPointF(1, 1))
        new_line = geometry.move_line_to_new_dot(
            QtCore.QPointF(100, 100), old_line)
        self.assertEqual(new_line.angle(), old_line.angle())
        self.assertEqual(new_line.p1(), QtCore.QPointF(100, 100))
        self.assertTrue(
            (math.fabs(new_line.length() - old_line.length())) <
            0.0001)

    # add testing for function create_line_by_pars
    def test_lines_functions(self):
        self.assertTrue(geometry.create_line_by_pars((1, 2, 3)) is None)
        line = geometry.create_line_by_pars((-7, 1))
        self.assertTrue(geometry.check_point_belongs_to_line(
            line,
            QtCore.QPointF(0, 1)))
        self.assertFalse(geometry.check_point_belongs_to_line(
            line,
            QtCore.QPointF(-200, -100)))
        self.assertFalse(geometry.check_point_belongs_to_line(
            line,
            QtCore.QPointF(200, 100)))
        self.assertTrue(
            geometry.check_line_contains_point(
                QtCore.QLineF(
                    QtCore.QPointF(0, 0),
                    QtCore.QPointF(100, 100)),
                QtCore.QPointF(1, 1)))
        self.assertTrue(
            geometry.check_line_contains_point(
                QtCore.QLineF(
                    QtCore.QPointF(0, 0),
                    QtCore.QPointF(100, 100)),
                QtCore.QPointF(-0.00000001, -0.00000001)))
        self.assertFalse(
            geometry.check_line_contains_point(
                QtCore.QLineF(
                    QtCore.QPointF(0, 0),
                    QtCore.QPointF(100, 100)),
                QtCore.QPointF(-1, -1)))
        line = geometry.create_line_by_pars((-7,))
        self.assertTrue(geometry.check_point_belongs_to_line(
            line,
            QtCore.QPointF(-7.0000001, 1)))
        self.assertFalse(geometry.check_point_belongs_to_line(
            line,
            QtCore.QPointF(-200, -100)))
        self.assertTrue(geometry.check_point_belongs_to_line(
            line,
            QtCore.QPointF(-6.999999999, 1.000000001)))


if __name__ == '__main__':
    unittest.main()
