from PyQt5 import QtCore, QtGui
from battle_field.common import functions
import logging

LOG = logging.getLogger(__name__)


class BumpCheckerNew():

    # return position: QtCore.QPointF()
    def bump_reaction(self, asker):
        filtered_items = self.colliding_no_relatives(asker)
        moving_vector = QtGui.QVector2D()
        for item in filtered_items:
            moving_vector += self.moving_vector(asker, item)
        new_pos = (
            QtCore.QPointF(
                asker.pos().x() +
                moving_vector.x(),
                asker.pos().y() +
                moving_vector.y()))
        LOG.critical("old_pos: %s, new_pos: %s" % (asker.pos(), new_pos))
        return new_pos

    # return only non relatives items (not parents, not childs)
    def colliding_no_relatives(self, asker):
        colliding_items = asker.scene().collidingItems(asker)
        return functions.remove_parents_and_childs(
            asker, colliding_items)

    # return Vector2D - vector of moving
    def moving_vector(self, asker, obst):
        normal_characteristic = []
        normals = self.normals_for_edges(obst, asker)
        intersection_dots = self.lines_intersections(asker, obst)
        all_asker_lines = functions.find_all_lines(asker)
        all_asker_dots = []
        for asker_line in all_asker_lines:
            all_asker_dots.append(asker_line.p1())
        asker_dots_in_obst = []
        asker_eject_vects = []
        for asker_dot in all_asker_dots:
            if (obst.contains(
                    asker_dot) and asker_dot not in asker_dots_in_obst):
                asker_dots_in_obst.append(asker_dot)

        for normal in normals:
            LOG.critical("asker_dots_in_obst: %s" % (asker_dots_in_obst, ))
            for asker_dot_in_obst in asker_dots_in_obst:
                asker_eject_vects.append(
                    self.ejection_vect_for_single_dot(
                        asker_dot_in_obst, normal))
            LOG.critical("intersection_dots: %s" % (intersection_dots, ))
            for intersection_dot in intersection_dots:
                asker_eject_vects.append(
                    self.ejection_vect_for_single_dot(
                        intersection_dot, normal))
            asker_eject_vects = sorted(
                asker_eject_vects,
                key=lambda value: (value.length()))
            LOG.critical("normal: %s, eject for normal: %s" % (
                normal, asker_eject_vects, ))
            normal_characteristic.append(
                asker_eject_vects[-1])
        normal_characteristic = sorted(
            normal_characteristic,
            key=lambda value: (value.length()))
        return normal_characteristic[0]

    # return [norm_line_1, norm_line_2, ...]
    # normal_line = QLineF
    # return normal lines only for intersected lines
    def normals_for_edges(self, obst, asker):
        normals = []
        obst_lines = functions.find_all_lines(obst)
        asker_lines = functions.find_all_lines(asker)
        dot_intersect = QtCore.QPointF()
        # check if obst fully contains line
        for obst_line in obst_lines:
            if (obst.contains(
                    obst_line.p1()) and obst.contains(
                        obst_line.p2())):
                normal = obst_line.normalVector()
                normal.setAngle(normal.angle() + 180)
                if normal not in normals:
                    normals.append(normal)
        # check if obstacle intersect line
        for obst_line in obst_lines:
            for asker_line in asker_lines:
                intersect_type = obst_line.intersect(
                    asker_line,
                    dot_intersect)
                if QtCore.QLineF.BoundedIntersection == intersect_type:
                    normal = obst_line.normalVector()
                    normal.setAngle(normal.angle() + 180)
                    if normal not in normals:
                        normals.append(normal)
        # check if no normal in our list, so add all normals,
        # because obstackle bigger and fully contains asker
        if len(normals) == 0:
            for obst_line in obst_lines:
                normal = obst_line.normalVector()
                normal.setAngle(normal.angle() + 180)
                if normal not in normals:
                    normals.append(normal)
        return normals

   # do not need this function?
    def filter_normal_by_centers_correllation(
            self, normals, asker, obst):
        normals_filtered = []
        centers_vect = QtGui.QVector2D(
            asker.pos() - obst.pos())
        for normal in normals:
            if int(QtGui.QVector2D.dotProduct(
                centers_vect,
                QtGui.QVector2D(
                    normal.p2() - normal.p1()))) >= 0:
                normals_filtered.append(normal)
        return normals_filtered

    def ejection_vects_for_item_dots(self, item, obst, direction):
        item_lines = functions.find_all_lines(item)
        ejection_vects = []
        for line in item_lines:
            if obst.contains(line.p1()):
                ejection_vects.append(
                    self.ejection_vect_for_single_dot(
                        line.p1(),
                        direction))
        return ejection_vects

    def ejection_vect_for_single_dot(self, dot, direction):
        perp_line = QtCore.QLineF(
            dot,
            QtCore.QPointF(0, 0))
        intersect_dot = QtCore.QPointF()
        perp_line.setAngle(direction.angle() + 90)
        perp_line.intersect(
            direction,
            intersect_dot)
        return QtGui.QVector2D(
            QtCore.QPointF(
                direction.p1().x() - intersect_dot.x(),
                direction.p1().y() - intersect_dot.y()))

    # function find intersections of two objects lines
    def lines_intersections(self, asker, obstacle):
        asker_lines = functions.find_all_lines(asker)
        obstacle_lines = functions.find_all_lines(obstacle)
        dots = []
        dot_intersect = QtCore.QPointF()
        for asker_line in asker_lines:
            for obstacle_line in obstacle_lines:
                intersect_type = asker_line.intersect(
                    obstacle_line,
                    dot_intersect)
                if ((QtCore.QLineF.BoundedIntersection == intersect_type) and (
                        dot_intersect not in dots)):
                    LOG.critical("append: %s by lines ask line: %s and obst line: %s" % (
                        dot_intersect,
                        asker_line,
                        obstacle_line))
                    dots.append(dot_intersect)
        return dots

    # return (QPointF, QPointF) - first point - dot of asker
    # second point -> belongs to one of lines
    def intersect_single_dot_with_lines(self, dot, direction, lines):
        # make for dot direction line:
        dot_line = QtCore.QLineF()
        dot_line.setP1(dot)
        dot_line.setLength(1)
        dot_line.setAngle(direction.angle())
        dots_wrapped = []
        dot_intersect = QtCore.QPointF()
        for line in lines:
            dot_line.intersect(
                line,
                dot_intersect)
            if functions.check_point_belongs_to_line(
                    line, dot_intersect):
                dots_wrapped.append()





