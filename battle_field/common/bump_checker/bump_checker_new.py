from PyQt5 import QtCore, QtGui
from battle_field.common import functions
from battle_field.common import geometry
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
        strategic_dots += geometry.intersect_by_secant(
            item_line.p1(), secant_line, asker_lines)
        for strategic_dot in strategic_dots:
            moving_lines.append(
                QtCore.QLineF(
                    strategic_dot, item_line.p1()))
        strategic_dots = []
        strategic_dots += geometry.intersect_by_secant(
            item_line.p2(), secant_line, asker_lines)
        for strategic_dot in strategic_dots:
            moving_lines.append(
                QtCore.QLineF(
                    strategic_dot, item_line.p2()))
        for asker_dot in asker_dots:
            intersect_dots = geometry.intersect_by_secant(
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
