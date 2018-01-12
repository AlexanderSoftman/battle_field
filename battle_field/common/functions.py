import math
import logging

from PyQt5.QtCore import QLineF, QPointF
from PyQt5.QtGui import QPolygonF
rounding_error = 0.00001

LOG = logging.getLogger(__name__)


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
        return True
    else:
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


# function filter items in vision
# will be removed - all our parents and all childs of our parents
def remove_parents_and_childs(item, not_filtered_items):
    filtered_items = list(not_filtered_items)
    # 1. find top parent of carrier_item
    top_parent = item
    while top_parent.parentItem() is not None:
        top_parent = top_parent.parentItem()
    # top_parent now is a top parent
    not_checked_items = []
    not_checked_items.append(top_parent)
    while len(not_checked_items) != 0:
        try:
            childs = not_checked_items[0].childItems()
            if childs is not None:
                not_checked_items.extend(childs)
        except AttributeError:
            pass
        try:
            filtered_items.remove(
                not_checked_items[0])
        except ValueError:
            pass
        except AttributeError:
            pass
        not_checked_items.remove(not_checked_items[0])
    return filtered_items
