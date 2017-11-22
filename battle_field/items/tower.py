import os
import math
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from battle_field.items import bullet
from battle_field.items import tank
from battle_field.common import functions
from battle_field.items import obstacle
from battle_field.items import lidar

import battle_field


class Tower(QtWidgets.QGraphicsPixmapItem):
    tower_picture_path = os.path.join(
        os.path.split(battle_field.__file__)[0], 'images/head.png')

    def __init__(self, scene, parent, bot_flag=True):
        super(Tower, self).__init__(parent)
        self.parent = parent
        self.rotation_speed_maximum = 5
        self.rotation_speed = 0
        self.setPixmap(QtGui.QPixmap(self.tower_picture_path))
        self.setOffset(
            - self.boundingRect().width() / 2,
            - self.boundingRect().height() / 2)
        self.setScale(0.9)
        self.last_shoot_time = scene.time.elapsed()
        self.last_angle_time = scene.time.elapsed()
        self.shoot_period = 7000
        self.angle_period = 7000
        self.destination_angle = self.rotation()
        self.safety_distance = 400
        self.vision_distance = 5000
        # debug only small value
        # self.vision_distance = 3000
        self.vision_ideal = QtGui.QPolygonF([
            QtCore.QPointF(0, 0),
            QtCore.QPointF(self.vision_distance, - self.vision_distance / 2),
            QtCore.QPointF(self.vision_distance, self.vision_distance / 2)])
        self.vision_shape = self.vision_ideal
        self.shadow_shape_list = []
        self.shadow_brush = QtGui.QBrush(
            QtGui.QColor(210, 210, 210, 20),
            QtCore.Qt.SolidPattern)
        self.vision = QtWidgets.QGraphicsPolygonItem(
            self.vision_shape,
            self)
        self.vision_lines = []
        self.vision_lines.append(
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(
                    self.vision_distance, - self.vision_distance / 2)))
        self.vision_lines.append(
            QtCore.QLineF(
                QtCore.QPointF(0, 0),
                QtCore.QPointF(
                    self.vision_distance, self.vision_distance / 2)))
        self.lidar = lidar.Lidar(
            self,
            30,
            10,
            60,
            180,
            2 * 6000,
            None)
        self.behind_line = QtCore.QLineF(
            QtCore.QPointF(self.vision_distance, - self.vision_distance / 2),
            QtCore.QPointF(self.vision_distance, self.vision_distance / 2))
        self.vision_lines.append(self.behind_line)
        self.bot_flag = bot_flag

    # interface
    def increase_rotation_speed(self):
        self.rotation_speed += 0.1 * self.rotation_speed_maximum
        if self.rotation_speed > self.rotation_speed_maximum:
            self.rotation_speed = self.rotation_speed_maximum

    # interface
    def reduce_rotation_speed(self):
        self.rotation_speed -= 0.1 * self.rotation_speed_maximum
        if math.fabs(self.rotation_speed) > self.rotation_speed_maximum:
            self.rotation_speed = -self.rotation_speed_maximum

    #   interface
    def create_bullet(self):
        if self.scene().time.elapsed() - self.last_shoot_time > \
                self.shoot_period:
            Bullet_x = self.boundingRect().width()
            Bullet_y = 0
            self.scene().addItem(bullet.Bullet(
                self.scene(),
                self.mapToScene(QtCore.QPointF(Bullet_x, Bullet_y)),
                self.parentItem().rotation() + self.rotation(),
                self.parentItem().speed))
            self.last_shoot_time = self.scene().time.elapsed()

    # internal for tower, called by timer
    def update(self):
        # self.update_vision()
        # move to tank level
        if (self.bot_flag):
            self.enemy()
            # self.change_angle()
            self.destroy()
        else:
            self.rotate_tower()

    # internal for tower
    def update_vision(self):
        # 0. assign to vision_shape ideal vision
        self.vision.setVisible(False)
        self.vision_shape = QtGui.QPolygonF(self.vision_ideal)
        for shadow in self.shadow_shape_list:
            shadow.setParentItem(None)
        del self.shadow_shape_list[:]
        # 1. find all colliding with vision items
        items_in_vision_before_filtering = self.scene().collidingItems(
            self.vision)
        items_in_vision = []
        for item in items_in_vision_before_filtering:
            if (isinstance(item, obstacle.Obstacle)):
                items_in_vision.append(item)
        # sort list by distance
        if len(items_in_vision) == 0:
            # reset vision to ideal
            self.vision.setPolygon(self.vision_ideal)
            self.vision.setVisible(True)
            return
        shadows = []
        for item in items_in_vision:
            all_lines_of_item = (
                functions.find_all_lines_in_my_sc(
                    item, self))
            # create item polygonf - need it later
            all_dots_of_item = []
            for line in all_lines_of_item:
                all_dots_of_item.append(line.p1())
            # item_shape_my_sc = QtGui.QPolygonF(all_dots_of_item)
            # 3. find lines only inside vision poligonf
            lines_in_vision = self.find_lines_in_ideal_vision(
                all_lines_of_item)
            # 4. find shadows for every item in vision
            # shadow_item = QtGui.QPolygonF()
            for line in lines_in_vision:
                # 4.1. find shadow for every line of item
                shadow_line = self.find_shadow(line)
                shadows.append(shadow_line)
        for shadow in shadows:
            self.shadow_shape_list.append(
                QtWidgets.QGraphicsPolygonItem(
                    shadow,
                    self))
            self.shadow_shape_list[-1].setPen(
                QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
            self.shadow_shape_list[-1].setBrush(self.shadow_brush)
            self.shadow_shape_list[-1].setVisible(True)
        # 5. assign current shape to PolygonItem
        self.vision.setPolygon(self.vision_shape)
        self.vision.setVisible(True)

    # internal for tower
    def find_shadow(self, line):
        behind_line_intersections = []
        point_of_intersection = QtCore.QPointF()
        intersection_type = QtCore.QLineF(
            line.p1(),
            QtCore.QPointF(0, 0)).intersect(
            self.behind_line, point_of_intersection)
        if (QtCore.QLineF.BoundedIntersection == intersection_type or
                QtCore.QLineF.UnboundedIntersection == intersection_type):
            behind_line_intersections.append(point_of_intersection)
        point_of_intersection = QtCore.QPointF()
        intersection_type = QtCore.QLineF(
            line.p2(),
            QtCore.QPointF(0, 0)).intersect(
            self.behind_line, point_of_intersection)
        if (QtCore.QLineF.BoundedIntersection == intersection_type or
                QtCore.QLineF.UnboundedIntersection == intersection_type):
            behind_line_intersections.append(point_of_intersection)
        return QtGui.QPolygonF(
            [behind_line_intersections[0],
                line.p1(),
                line.p2(),
                behind_line_intersections[1]])

    # internal for tower
    def find_lines_in_ideal_vision(self, lines):

        lines_in_vision = []
        # lines fully inside vision
        for line in lines:
            if (self.vision_ideal.containsPoint(
                line.p1(), QtCore.Qt.OddEvenFill) and
                    self.vision_ideal.containsPoint(
                        line.p2(), QtCore.Qt.OddEvenFill)):
                    lines_in_vision.append(line)
        # lines, part of which inside vision_ideal
        for line in lines:
            point_of_intersection_list = []
            for vision_line in self.vision_lines:
                point_of_intersection = QtCore.QPointF()
                intersection_type = vision_line.intersect(
                    line, point_of_intersection)
                if QtCore.QLineF.BoundedIntersection == intersection_type:
                    point_of_intersection_list.append(point_of_intersection)
            # check if we have 2 points of intersection
            # so should create line without start and end of first line
            if len(point_of_intersection_list) == 2:
                lines_in_vision.append(
                    QtCore.QLineF(
                        point_of_intersection_list[0],
                        point_of_intersection_list[1]))
            # check if we have 1 points of intersection
            # so should create line WITH start or end of first line
            if len(point_of_intersection_list) == 1:
                # find start or end inside vision_ideal
                if self.vision_ideal.containsPoint(
                        line.p1(), QtCore.Qt.OddEvenFill):
                    lines_in_vision.append(
                        QtCore.QLineF(
                            point_of_intersection_list[0],
                            line.p1()))
                elif self.vision_ideal.containsPoint(
                        line.p2(), QtCore.Qt.OddEvenFill):
                    lines_in_vision.append(
                        QtCore.QLineF(
                            point_of_intersection_list[0],
                            line.p2()))
        return lines_in_vision

    # internal for tower, bot only
    def enemy(self):
        # 1. search targets
        all_items_partly_in_vision_list = self.scene().collidingItems(
            self.vision, QtCore.Qt.IntersectsItemBoundingRect)
        # all_items_fully_in_vision_list = self.scene().collidingItems(
            # self.vision, QtCore.Qt.ContainsItemBoundingRect)
        targets_partly_in_vision_list = []
        # targets_fully_in_vision_list = []
        # filter targets to tanks
        for target in all_items_partly_in_vision_list:
            if (isinstance(target, tank.Tank) and
                    target is not self.parentItem()):
                targets_partly_in_vision_list.append(target)
        # for target in all_items_fully_in_vision_list:
            # if (isinstance(target, tank.Tank) and
                    # target is not self.parentItem()):
                # targets_fully_in_vision_list.append(target)
        # print("previos detected count of items fully in vision: %s" % (
            # len(targets_fully_in_vision_list),))
        # check all targets, at least partly in vision are not fully
        # in at least one of shapes
        for target in targets_partly_in_vision_list:
            for shadow in self.shadow_shape_list:
                # items_fully_inside_shadow = self.scene().collidingItems(
                    # shadow, QtCore.Qt.ContainsItemBoundingRect)
                items_partly_inside_shadow = self.scene().collidingItems(
                    shadow, QtCore.Qt.IntersectsItemBoundingRect)
                targets_partly_inside_shadow = []
                for item in items_partly_inside_shadow:
                    if (isinstance(item, tank.Tank) and
                            item is not self.parentItem()):
                        targets_partly_inside_shadow.append(item)
                if (target in targets_partly_inside_shadow and
                        target in targets_partly_in_vision_list):
                    print("one target in shadow, remove from targets_list")
                    targets_partly_in_vision_list.remove(target)
        enemies_info = []
        for target in targets_partly_in_vision_list:
            if (isinstance(target, Tower)):
                if target is self:
                    continue
                vect_to_target = QtGui.QVector2D(
                    target.mapToScene(0, 0) - self.mapToScene(0, 0))
                distance_to_target = vect_to_target.length()
                vect_to_target = vect_to_target.normalized()
                vect_of_body = QtGui.QVector2D(
                    (self.parentItem().mapToScene(1, 0)) -
                    (self.parentItem().mapToScene(0, 0))).normalized()
                angle_to_target = 180.0 * math.acos(
                    QtGui.QVector2D.dotProduct(
                        vect_to_target, vect_of_body)) / math.pi

                vect_of_body_orto = QtGui.QVector2D(
                    -vect_of_body.y(), vect_of_body.x())

                # get sign of angle
                sign = QtGui.QVector2D.dotProduct(
                    vect_to_target, vect_of_body_orto)
                angle_to_target = \
                    angle_to_target if sign > 0 else - angle_to_target

                enemies_info.append([
                    distance_to_target,
                    angle_to_target])

        # print(enemies_info)
        # 2. we should find tank with minimum
        # distance as most dangerous.most
        # But if distance is not so small,
        # we should find tank with our tower angle
        if len(enemies_info) == 0:
            self.start_scanning()
        else:
            # sort enemies by angle
            en_info_sorted = sorted(
                enemies_info, key=lambda x: math.fabs(x[1]))
            # default destination_angle - minimum value
            self.destination_angle = en_info_sorted[0][1]
            # check that we don't have enemy in safety area
            # it should be killed first
            for enemy in en_info_sorted:
                if (enemy[0] < self.safety_distance):
                    self.destination_angle = enemy[1]
                    break

    # internal for tower, bot only
    def start_scanning(self):
        # find new destination angle
        if self.scene().time.elapsed() - self.last_angle_time > \
                self.rotation():
            self.last_angle_time = self.scene().time.elapsed()
            self.angle_period = -45 + (QtCore.qrand() % 90)

    # internal for tower, bot only
    def change_angle(self):
        if (self.rotation() != self.destination_angle):
            if (self.destination_angle - self.rotation() > 0):
                sign = 1
            else:
                sign = -1
            self.setRotation(
                self.rotation() +
                sign * self.rotation_speed_maximum * self.scene().dt
            )

    # internal for tower, bot only
    def destroy(self):
        if (math.fabs(self.rotation() - self.destination_angle) < 5):
            self.create_bullet()

    # internal for tower
    def rotate_tower(self):
        self.setRotation(
            self.rotation() +
            self.rotation_speed * self.scene().dt
        )
