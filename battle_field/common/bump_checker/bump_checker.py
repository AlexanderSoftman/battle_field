from PyQt5 import QtCore, QtGui
from battle_field.common import functions
from battle_field.common import geometry
import logging

LOG = logging.getLogger(__name__)


class BumpChecker():

    # return
    # position: QtCore.QPointF()
    def bump_check(self, asker):
        not_filtered_items = asker.scene().collidingItems(asker)
        # find all not child items!
        filtered_items = functions.remove_parents_and_childs(
            asker, not_filtered_items)
        push_away_list = [asker.pos()]
        for item in filtered_items:
            push_away_list.append(
                self.push_away(
                    asker, item))
        # wrong way - return only last value from push away list
        return push_away_list[-1]
        # process push away list

    # return
    # position: QtCore.QPointF()
    def push_away(self, asker, item):
        # new position default = current position
        new_pos = asker.pos()
        # 1. find all lines
        asker_all_lines = functions.find_all_lines(asker)
        item_all_lines = functions.find_all_lines(item)

        # 2. find colliding lines and dots
        asker_lines, asker_dots = self.find_colliding_lines_and_dots(
            asker_all_lines, item_all_lines, item)
        item_lines, item_dots = self.find_colliding_lines_and_dots(
            item_all_lines, asker_all_lines, asker)

        # 3. find move direction
        move_dir = self.find_moving_vect(
            asker_all_lines,
            item_all_lines,
            item)
        LOG.critical("move_dir: %s" % (move_dir,))

        # 4. for every my and item dot inside other object
        # create projection
        full_projection_list = []

        for asker_dot in asker_dots:
            # create parallel line:
            par_line = QtCore.QLineF(
                asker_dot,
                asker_dot + move_dir.toPointF())
            # find all collisions with all lines of item:
            dots_intersected = []
            dot_intersected = QtCore.QPointF()
            for item_line in item_lines:
                intersect_type = par_line.intersect(
                    item_line,
                    dot_intersected)
                # check unbounded and bounded intersection type
                if ((QtCore.QLineF.BoundedIntersection == intersect_type) or
                    (QtCore.QLineF.UnboundedIntersection == intersect_type) and
                    (
                        min(
                            item_line.pointAt(0).x(),
                            item_line.pointAt(1).x()) <=
                        dot_intersected.x() <=
                        max(
                            item_line.pointAt(0).x(),
                            item_line.pointAt(1).x())) and (
                        min(
                            item_line.pointAt(0).y(),
                            item_line.pointAt(1).y()) <=
                        dot_intersected.y() <=
                        max(
                            item_line.pointAt(0).y(),
                            item_line.pointAt(1).y())) and
                        geometry.check_point_belongs_to_line(
                            item_line, dot_intersected)):
                    dots_intersected.append(
                        QtCore.QPointF(
                            dot_intersected))
            # all item lines checked.
            # create list of projections vectors from
            # my point to direction
            dot_products_for_asker_dot = []
            for dot in dots_intersected:
                # print("dot = " + str(dot))
                vector = QtGui.QVector2D(
                    QtCore.QPointF(
                        dot.x() - asker_dot.x(),
                        dot.y() - asker_dot.y()))
                dot_products_for_asker_dot.append(
                    QtGui.QVector2D.dotProduct(vector, move_dir))
            # sort all dot product list
            dot_products_for_asker_dot = sorted(
                dot_products_for_asker_dot,
                key=lambda value: value)
            # check that list is not empty,
            # get maximum value (-1 element)
            if len(dot_products_for_asker_dot) > 0:
                full_projection_list.append(
                    dot_products_for_asker_dot[-1])
        # for every item dots create list of collision with my lines
        for item_dot in item_dots:
            # create parallel line:
            par_line = QtCore.QLineF(item_dot, item_dot + move_dir.toPointF())
            # find all collisions with all lines of item:
            dots_intersected = []
            dot_intersected = QtCore.QPointF()
            for asker_line in asker_lines:
                intersect_type = par_line.intersect(
                    asker_line,
                    dot_intersected)
                # check unbounded and bounded intersection type
                # check that QtCore.QPointF belongs to QtCore.QLineF
                if ((QtCore.QLineF.BoundedIntersection == intersect_type) or
                    (QtCore.QLineF.UnboundedIntersection == intersect_type) and
                    (
                        min(
                            asker_line.pointAt(0).x(),
                            asker_line.pointAt(1).x()) <=
                        dot_intersected.x() <=
                        max(
                            asker_line.pointAt(0).x(),
                            asker_line.pointAt(1).x())) and (
                        min(
                            asker_line.pointAt(0).y(),
                            asker_line.pointAt(1).y()) <=
                        dot_intersected.y() <=
                        max(
                            asker_line.pointAt(0).y(),
                            asker_line.pointAt(1).y()))):
                    # print("add new intersect dot = " + str(dot_intersected))
                    dots_intersected.append(
                        QtCore.QPointF(
                            dot_intersected))
            # all my lines checked.
            # create list of projections vectors from
            # item point to direction
            dot_products_for_item_dot = []
            for dot in dots_intersected:
                vector = QtGui.QVector2D(
                    item_dot - dot)
                dot_products_for_item_dot.append(
                    QtGui.QVector2D.dotProduct(vector, move_dir))
            # sort all dot product list
            dot_products_for_item_dot = sorted(
                dot_products_for_item_dot,
                key=lambda value: value)
            # check that list is not empty,
            # get maximum value (-1 element)
            if len(dot_products_for_item_dot) > 0:
                full_projection_list.append(
                    dot_products_for_item_dot[-1])

        # 8. sort full_projection_list by projection values
        full_projection_list = sorted(
            full_projection_list,
            key=lambda value: value)

        # 9. move to maximum value from full_projection_list[-1]
        if len(full_projection_list) > 0:
            new_pos += (move_dir * full_projection_list[-1]).toPointF()
        return new_pos

    def find_colliding_lines_and_dots(self, tested_list, second_list, item):
        lines_list = []
        dots_list = []
        point_of_intersection = QtCore.QPointF()
        # find bounded lines
        for test_line in tested_list:
            # add instersection dots
            for second_line in second_list:
                intersection_type = test_line.intersect(
                    second_line, point_of_intersection)
                if (QtCore.QLineF.BoundedIntersection == intersection_type and
                        test_line not in lines_list):
                    lines_list.append(QtCore.QLineF(test_line))

        # find lines fully inside item:
        rect = QtCore.QRectF(
            item.mapToScene(
                QtCore.QPointF(
                    - item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2)),
            item.mapToScene(
                QtCore.QPointF(
                    item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)))
        for test_line in tested_list:
            if (rect.contains(test_line.p1()) and
                rect.contains(test_line.p2()) and
                    test_line not in lines_list):
                lines_list.append(test_line)

        if len(lines_list) > 1:
            for first in lines_list:
                for second in lines_list:
                    if first != second:
                        if (first.p1() == second.p1() or
                            first.p1() == second.p2() and
                                first.p1() not in dots_list):
                                dots_list.append(first.p1())
                        if (first.p2() == second.p1() or
                            first.p2() == second.p2() and
                                first.p2() not in dots_list):
                                dots_list.append(first.p2())

        return lines_list, dots_list

    def find_moving_vect(self, my_lines, obj_lines, item):
        all_dots_list = []
        point_of_intersection = QtCore.QPointF()
        # find bounded lines
        for my_line in my_lines:
            # add instersection dots
            for obj_line in obj_lines:
                intersection_type = my_line.intersect(
                    obj_line, point_of_intersection)
                if QtCore.QLineF.BoundedIntersection == intersection_type:
                    all_dots_list.append(QtCore.QPointF(point_of_intersection))
        # find lines fully inside me:
        rect = QtCore.QRectF(
            item.mapToScene(
                QtCore.QPointF(
                    - item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2)),
            item.mapToScene(
                QtCore.QPointF(
                    item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)))

        for obj_line in obj_lines:
            if (rect.contains(obj_line.p1()) and
                    rect.contains(obj_line.p2())):
                all_dots_list.append(obj_line.p1())
                all_dots_list.append(obj_line.p2())

        # sort list of dots
        all_dots_list = sorted(
            all_dots_list,
            key=lambda value: (QtCore.QLineF(
                QtCore.QPointF(0, 0),
                item.mapToItem(item, value)).angle()))

        normal_lines = []
        for idx_first, dot_first in enumerate(all_dots_list):
            for idx_second, dot_second in enumerate(all_dots_list):
                if (idx_first == idx_second + 1 or
                    (idx_first == len(all_dots_list) - 1 and
                        idx_second == 0)):
                    normal_lines.append(
                        QtCore.QLineF(
                            dot_first,
                            dot_second).normalVector())
        normal_lines = sorted(
            normal_lines,
            key=lambda value: value.length())
        LOG.critical("normal_lines sorted: %s" % (normal_lines,))
        return QtGui.QVector2D(
            normal_lines[-1].p2() - normal_lines[-1].p1()).normalized()
