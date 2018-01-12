from PyQt5 import QtCore
from battle_field.common import functions
import logging

LOG = logging.getLogger(__name__)


# find all dots (
# that found with intersect by secant line lines with dots)
def intersect_by_secant(
        dot,
        arbitrary_secant_line,
        lines_with_dots,
        check_line_contain_point=True):
    secant_line = move_line_to_new_dot(
        dot, arbitrary_secant_line)
    follow_up_dots = []
    for line_with_dot in lines_with_dots:
        dot_intersect = QtCore.QPointF()
        intersect_type = secant_line.intersect(
            line_with_dot, dot_intersect)
        if (((QtCore.QLineF.BoundedIntersection ==
            intersect_type) or (
                QtCore.QLineF.UnboundedIntersection ==
                intersect_type)) and (
                dot_intersect not in follow_up_dots)):
            if (check_line_contain_point is True):
                if check_line_contains_point(
                        line_with_dot, dot_intersect):
                    follow_up_dots.append(dot_intersect)
            else:
                follow_up_dots.append(dot_intersect)
    return follow_up_dots


def move_line_to_new_dot(dot, line):
    new_line = QtCore.QLineF(
        dot,
        dot + QtCore.QPointF(1, 1))
    new_line.setLength(
        line.length())
    new_line.setAngle(
        line.angle())
    return new_line


# input: (k, b) if y = kx+b
# or (x) if x = 3
# return QLineF or None
def create_line_by_pars(line_parameters):
    line = QtCore.QLineF()
    if len(line_parameters) == 1:
        line = QtCore.QLineF(
            QtCore.QPointF(line_parameters[0], 0),
            QtCore.QPointF(line_parameters[0], 1))
    elif len(line_parameters) == 2:
        line = QtCore.QLineF(
            QtCore.QPointF(0, line_parameters[1]),
            QtCore.QPointF(
                1, line_parameters[0] + line_parameters[1]))
    else:
        line = None
    return line


def check_point_belongs_to_line(line, some_point):
    # y = kx + b
    # find k and b:
    # if x1 == x2 => line is x = number
    if line.x1() - line.x2() != 0:
        k = (
            (line.y1() - line.y2()) /
            (line.x1() - line.x2()))
        b = line.y1() - k * line.x1()
        if functions.check_equality_with_rounding(
                k * some_point.x() + b, some_point.y()):
            return True
        else:
            return False
    else:
        if (functions.check_equality_with_rounding(
                line.x1(), some_point.x()) and (
                some_point.y() >= min(
                    line.y1(),
                    line.y2()) - functions.rounding_error) and (
                some_point.y() <= max(
                    line.y1(),
                    line.y2()) + functions.rounding_error)):
            return True
        else:
            return False


def check_line_contains_point(line, some_point):
    if (
        check_point_belongs_to_line(line, some_point) and (
            some_point.x() >= (
                min(line.x1(), line.x2()) -
                functions.rounding_error)) and (
            some_point.x() <= (
                max(line.x1(), line.x2()) +
                functions.rounding_error)) and (
            some_point.y() >= (
                min(line.y1(), line.y2()) -
                functions.rounding_error)) and (
            some_point.y() <= (
                max(line.y1(), line.y2()) +
                functions.rounding_error))):
        return True
    else:
        return False
