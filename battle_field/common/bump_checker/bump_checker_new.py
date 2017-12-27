from PyQt5 import QtCore, QtGui
from battle_field.common import functions
import logging

LOG = logging.getLogger(__name__)


class BumpCheckerNew():
    # return position: QtCore.QPointF()

    def bump_reaction(self, asker):
        filtered_items = self.colliding_no_relatives(asker)
        new_pos = asker.pos()
        asker_lines = functions.find_all_lines(asker)
        for item in filtered_items:
            moving_lines = []
            item_lines = functions.find_all_lines(item)
            for item_line in item_lines:
                mov_line = self.moving_line(asker_lines, item_line)
                if mov_line is not None:
                    moving_lines.append(mov_line)
            if len(moving_lines) > 0:
                # sort by length, get minimum length
                moving_lines = sorted(
                    moving_lines,
                    key=lambda line: line.length())
                new_pos = (
                    asker.pos() +
                    moving_lines[0].p2() -
                    moving_lines[0].p1())
            return new_pos
        return new_pos

    # return only non relatives items (not parents, not childs)
    def colliding_no_relatives(self, asker):
        colliding_items = asker.scene().collidingItems(asker)
        return functions.remove_parents_and_childs(
            asker, colliding_items)

    # return Vector2D - vector of moving
    def moving_line(self, asker_lines, item_line):
        not_filtered_lines = []
        moving_lines = []
        # 1. find secant line
        secant_line = item_line.normalVector()
        secant_line.setAngle(secant_line.angle() + 180)
        # 2. find asker dots
        asker_dots = []
        for line in asker_lines:
            asker_dots.append(line.p1())
        # 3. create virtual pipe and find intersections pipe and asker dots
        # and asker dots inside pipe
        strategic_dots = []
        strategic_dots += self.intersect_by_secant(
            item_line.p1(), secant_line, asker_lines)
        for strategic_dot in strategic_dots:
            moving_lines.append(
                QtCore.QLineF(
                    strategic_dot, item_line.p1()))
        strategic_dots = []
        strategic_dots += self.intersect_by_secant(
            item_line.p2(), secant_line, asker_lines)
        for strategic_dot in strategic_dots:
            moving_lines.append(
                QtCore.QLineF(
                    strategic_dot, item_line.p2()))
        for asker_dot in asker_dots:
            intersect_dots = self.intersect_by_secant(
                asker_dot, secant_line, [item_line])
            for intersect_dot in intersect_dots:
                moving_lines.append(
                    QtCore.QLineF(
                        asker_dot, intersect_dot))
        # 4. sort by length and remove negative dot products
        not_negative_moving_lines = []
        for moving_line in moving_lines:
            if QtGui.QVector2D.dotProduct(
                    QtGui.QVector2D(
                        secant_line.p2() - secant_line.p1()),
                    QtGui.QVector2D(
                        moving_line.p2() - moving_line.p1())) > 0:
                not_negative_moving_lines.append(moving_line)
            elif moving_line.isNull():
                not_negative_moving_lines.append(
                    QtCore.QLineF(
                        QtCore.QPointF(0, 0),
                        QtCore.QPointF(0, 0)))
            else:
                not_filtered_lines.append(moving_line)
        not_negative_moving_lines = sorted(
            not_negative_moving_lines,
            key=lambda line: line.length())
        if len(not_negative_moving_lines) > 0:
            return not_negative_moving_lines[-1]
        else:
            return None

    def move_line_to_new_dot(self, dot, line):
        new_line = QtCore.QLineF(
            dot,
            dot + QtCore.QPointF(1, 1))
        new_line.setLength(
            line.length())
        new_line.setAngle(
            line.angle())
        return new_line

    # find all dots (
    # that found with intersect by secant line lines with dots)
    def intersect_by_secant(
            self, dot, arbitrary_secant_line, lines_with_dots):
        secant_line = self.move_line_to_new_dot(
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
                    dot_intersect not in follow_up_dots) and (
                    functions.check_line_contains_point(
                        line_with_dot, dot_intersect))):
                follow_up_dots.append(dot_intersect)
        return follow_up_dots
