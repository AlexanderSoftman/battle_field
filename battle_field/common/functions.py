import math
import logging

from PyQt5.QtCore import QLineF, QPointF
from PyQt5.QtGui import QPolygonF
rounding_error = 0.00001

LOG = logging.getLogger(__name__)


def check_point_belongs_to_line(line, some_point):
    # y = kx + b
    # find k and b:
    # if x1 == x2 => line is x = number
    if line.x1() != line.x2():
        k = (
            (line.y1() - line.y2()) /
            (line.x1() - line.x2()))
        b = line.y1() - k * line.x1()
        if check_equality_with_rounding(
                k * some_point.x() + b, some_point.y()):
            return True
        else:
            return False
    else:
        if (check_equality_with_rounding(
                line.x1(), some_point.x()) and
            some_point.y() >= min(
                line.y1(),
                line.y2() - rounding_error) and
            some_point.y() <= max(
                line.y1(),
                line.y2()) + rounding_error):
            # LOG.debug(
                # "point %s belongs to line: %s" % (
                    # some_point, line))
            return True
        else:
            # LOG.debug(
                # "point %s NOT belongs to line: %s" % (
                    # some_point, line))
            return False


def check_line_contains_point(line, some_point):
    if (
        check_point_belongs_to_line(line, some_point) and (
            some_point.x() >= (
                min(line.x1(), line.x2()) -
                rounding_error)) and (
            some_point.x() <= (
                max(line.x1(), line.x2()) +
                rounding_error)) and (
            some_point.y() >= (
                min(line.y1(), line.y2()) -
                rounding_error)) and (
            some_point.y() <= (
                max(line.y1(), line.y2()) +
                rounding_error))):
        return True
    else:
        return False


def find_all_lines(item):

    parts_of_item = []
    # 1. find all lines of item in scene coordinates:
    # top line
    parts_of_item.append(
        QLineF(
            item.mapToScene(
                QPointF(
                    item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2)),
            item.mapToScene(
                QPointF(
                    - item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2))))

    # left line
    parts_of_item.append(
        QLineF(
            item.mapToScene(
                QPointF(
                    - item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2)),
            item.mapToScene(
                QPointF(
                    - item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2))))

    # bottom line
    parts_of_item.append(
        QLineF(
            item.mapToScene(
                QPointF(
                    - item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)),
            item.mapToScene(
                QPointF(
                    item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2))))

    # right line
    parts_of_item.append(
        QLineF(
            item.mapToScene(
                QPointF(
                    item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)),
            item.mapToScene(
                QPointF(
                    item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2))))

    # for part in parts_of_item:
    # print("part len = " + str(part.length()))
    return parts_of_item


# return list of QLineF: [QLineF1, QLineF2 ...]
def find_all_lines_in_my_sc(item, me):

    parts_of_item = []
    # 1. find all lines of item in scene coordinates:
    # top line
    parts_of_item.append(
        QLineF(
            item.mapToItem(
                me,
                QPointF(
                    item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2)),
            item.mapToItem(
                me,
                QPointF(
                    - item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2))))

    # left line
    parts_of_item.append(
        QLineF(
            item.mapToItem(
                me,
                QPointF(
                    - item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2)),
            item.mapToItem(
                me,
                QPointF(
                    - item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2))))

    # bottom line
    parts_of_item.append(
        QLineF(
            item.mapToItem(
                me,
                QPointF(
                    - item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)),
            item.mapToItem(
                me,
                QPointF(
                    item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2))))

    # right line
    parts_of_item.append(
        QLineF(
            item.mapToItem(
                me,
                QPointF(
                    item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)),
            item.mapToItem(
                me,
                QPointF(
                    item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2))))

    # for part in parts_of_item:
    # print("parts_of_item = %s" % (parts_of_item, ))
    return parts_of_item


def find_poligon(item):

    dots_of_item = []
    dots_of_item.append(
        item.mapToScene(
            QPointF(
                item.boundingRect().width() / 2,
                - item.boundingRect().height() / 2)))
    dots_of_item.append(
        item.mapToScene(
            QPointF(
                - item.boundingRect().width() / 2,
                - item.boundingRect().height() / 2)))
    dots_of_item.append(
        item.mapToScene(
            QPointF(
                - item.boundingRect().width() / 2,
                item.boundingRect().height() / 2)))
    dots_of_item.append(
        item.mapToScene(
            QPointF(
                item.boundingRect().width() / 2,
                item.boundingRect().height() / 2)))

    return QPolygonF(dots_of_item)


def check_equality_with_rounding(first, second):
    if (
        math.fabs(
            first - second) <= rounding_error):
        # LOG.debug("%s equals to %s" % (
            # first, second))
        return True
    else:
        # LOG.debug("%s NOT equals to %s" % (
            # first, second))
        return False


def point_in_list(test_point, test_list):
    for point in test_list:
        if (test_point.x() == point.x() and
                test_point.y() == point.y()):
            return True
    return False


def remove_duplicate_points(test_polygon):
    result_points_list = []
    first_point_flag = False
    for point in test_polygon:
        if (point not in result_points_list):
            result_points_list.append(point)
        if (point in result_points_list and
                first_point_flag is False):
            result_points_list.append(point)
            first_point_flag = True
    return QPolygonF(result_points_list)
