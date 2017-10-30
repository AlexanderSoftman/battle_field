import math

from PyQt5.QtCore import QLineF, QPointF
from PyQt5.QtGui import QPolygonF

rounding_error = 0.00001


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
            # print("first_case::point belong to line")
            return True
        else:
            #print("first_case::point doesn't belong to line")
            return False
    else:
        if (check_equality_with_rounding(
                line.x1(), some_point.x()) and
            some_point.y() >= min(
                line.y1(),
                line.y2()) and
            some_point.y() <= max(
                line.y1(),
                line.y2())):
            #print("second_case::point belong to line")
            return True
        else:
            #print("second_case::point doesn't belong to line")
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
    # print("part len = " + str(part.length()))
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
        return True
    else:
        return False
