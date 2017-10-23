
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsRectItem
from PyQt5.QtCore import qrand, QRectF, QLineF, QPointF
from PyQt5.QtGui import QPixmap, QVector2D

import math

from tower import Tower
from obstacle import Obstacle


class Personage(QGraphicsPixmapItem):

    tank_picture_path = './src/images/tank_3.png'

    def __init__(self, scene, pos, angle, bot_flag=True):
        QGraphicsPixmapItem.__init__(self)
        self.rect = QGraphicsRectItem(QRectF(0, 0, 10, 10), self)
        self.setPos(pos)
        self.setRotation(angle)
        self.speed = 10
        self.body_rotation_speed = 20
        self.setPixmap(QPixmap(self.tank_picture_path))
        self.setOffset(
            - self.boundingRect().width() / 2,
            - self.boundingRect().height() / 2)
        self.setScale(0.15)
        self.last_angle_time = scene.time.elapsed()
        self.body_angle_period = 6000 + qrand() % 5000
        self.destination_angle = self.rotation()
        self.tower = Tower(scene, self, bot_flag)
        self.bot_flag = bot_flag

    def increase_speed(self):
        self.speed += 1

    def reduce_speed(self):
        self.speed -= 1

    def increase_angle(self):
        self.setRotation(
            self.rotation() + 2)

    def reduce_angle(self):
        self.setRotation(
            self.rotation() - 2)

    def update(self):
        self.change_pos()
        self.bump_check()
        if self.bot_flag:
            self.add_new_angle()
            self.change_angle()

    def change_pos(self):
        x = self.pos().x() + self.speed * math.cos(
            self.rotation() * math.pi / 180.0) * self.scene().dt
        y = self.pos().y() + self.speed * math.sin(
            self.rotation() * math.pi / 180.0) * self.scene().dt
        self.setPos(x, y)

    def add_new_angle(self):
        if self.scene().time.elapsed() - self.last_angle_time > \
                self.body_angle_period:
            self.last_angle_time = self.scene().time.elapsed()
            self.destination_angle = -45 + (qrand() % 90)

    def change_angle(self):
        if (self.rotation() != self.destination_angle):
            if (self.destination_angle - self.rotation() > 0):
                sign = 1
            else:
                sign = -1
            self.setRotation(
                self.rotation() +
                sign * self.body_rotation_speed * self.scene().dt
            )

    def bump_check(self):
        item_list = self.scene().collidingItems(self)
        for item in item_list:
            if (isinstance(item, Personage) and item is not self or
                    isinstance(item, Obstacle)):
                self.move_us(item)

    def move_us(self, item):

        # 1. find all lines
        my_all_lines = self.find_all_lines(self)
        item_all_lines = self.find_all_lines(item)
        # for my_line in my_all_lines:
            # print("my_line = " + str(my_line))
        # for item_line in item_all_lines:
            # print("item_line = " + str(item_line))

        # 2. find colliding lines and dots
        my_lines, my_dots = self.find_colliding_lines_and_dots(
            my_all_lines, item_all_lines, item)
        item_lines, item_dots = self.find_colliding_lines_and_dots(
            item_all_lines, my_all_lines, self)

        # for my_line in my_lines:
            # print("colliding my_line = " + str(my_line))
        # for item_line in item_lines:
            # print("colliding item_line = " + str(item_line))

        # for my_dot in my_dots:
            # print("my_dot in item = " + str(my_dot))
        # for item_dot in item_dots:
            # print("item_dot in my = " + str(item_dot))

        # 3. find move direction
        move_dir = self.find_moving_vect(my_all_lines, item_all_lines, item)
        # 4. for every my and item dot inside other object
        # create projection
        full_projection_list = []

        for my_dot in my_dots:
            # print ("my dot = " + str(my_dot))
            # create parallel line:
            par_line = QLineF(my_dot, my_dot + move_dir.toPointF())
            # print ("par line for my dot = " + str(par_line))
            # find all collisions with all lines of item:
            dots_intersected = []
            dot_intersected = QPointF()
            for item_line in item_lines:
                intersect_type = par_line.intersect(item_line, dot_intersected)
                # check unbounded and bounded intersection type
                if ((QLineF.BoundedIntersection == intersect_type) or
                    (QLineF.UnboundedIntersection == intersect_type) and (
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
                        self.check_point_belongs_to_line(
                            item_line, dot_intersected)):
                    # print ("add new intersect dot = " + str(dot_intersected))
                    dots_intersected.append(QPointF(dot_intersected))
            # all item lines checked.
            # create list of projections vectors from
            # my point to direction
            dot_products_for_my_dot = []
            for dot in dots_intersected:
                # print("dot = " + str(dot))
                vector = QVector2D(
                    QPointF(
                        dot.x() - my_dot.x(),
                        dot.y() - my_dot.y()))
                dot_products_for_my_dot.append(
                    QVector2D.dotProduct(vector, move_dir))
                # print("add dot product = " + str(
                    # QVector2D.dotProduct(vector, move_dir)))
            # sort all dot product list
            dot_products_for_my_dot = sorted(
                dot_products_for_my_dot,
                key=lambda value: value)
            # print("dot_products_for_my_dot sorted = " + str(
                # dot_products_for_my_dot))
            # check that list is not empty,
            # get maximum value (-1 element)
            if len(dot_products_for_my_dot) > 0:
                full_projection_list.append(
                    dot_products_for_my_dot[-1])
            # print("add to full projection maximum projection: " + str(
                # dot_products_for_my_dot[-1]))
        # for every item dots create list of collision with my lines
        for item_dot in item_dots:
            # print("item_dot = " + str(item_dot))
            # create parallel line:
            par_line = QLineF(item_dot, item_dot + move_dir.toPointF())
            # print("par_line for item_dot = " + str(par_line))
            # find all collisions with all lines of item:
            dots_intersected = []
            dot_intersected = QPointF()
            for my_line in my_lines:
                intersect_type = par_line.intersect(my_line, dot_intersected)
                # check unbounded and bounded intersection type
                # check that QPointF belongs to QLineF
                if ((QLineF.BoundedIntersection == intersect_type) or
                    (QLineF.UnboundedIntersection == intersect_type) and (
                        min(
                            my_line.pointAt(0).x(),
                            my_line.pointAt(1).x()) <=
                        dot_intersected.x() <=
                        max(
                            my_line.pointAt(0).x(),
                            my_line.pointAt(1).x())) and (
                        min(
                            my_line.pointAt(0).y(),
                            my_line.pointAt(1).y()) <=
                        dot_intersected.y() <=
                        max(
                            my_line.pointAt(0).y(),
                            my_line.pointAt(1).y()))):
                    # print("add new intersect dot = " + str(dot_intersected))
                    dots_intersected.append(QPointF(dot_intersected))
            # all my lines checked.
            # create list of projections vectors from
            # item point to direction
            dot_products_for_item_dot = []
            for dot in dots_intersected:
                vector = QVector2D(
                    item_dot - dot)
                dot_products_for_item_dot.append(
                    QVector2D.dotProduct(vector, move_dir))
                # print("add new dot_products_for_item_dot = " +
                    # str(QVector2D.dotProduct(vector, move_dir)))
            # sort all dot product list
            dot_products_for_item_dot = sorted(
                dot_products_for_item_dot,
                key=lambda value: value)
            # print("dot_products_for_item_dot sorted = " + str(
                # dot_products_for_item_dot))
            # check that list is not empty,
            # get maximum value (-1 element)
            if len(dot_products_for_item_dot) > 0:
                full_projection_list.append(
                    dot_products_for_item_dot[-1])

        # 8. sort full_projection_list by projection values
        full_projection_list = sorted(
            full_projection_list,
            key=lambda value: value)
        # print("full_projection_list sorted = " + str(
            # full_projection_list))

        # 9. move to maximum value from projection listfull_projection_list[-1]
        if len(full_projection_list) > 0:
            # print("pos before moving = " + str(self.pos()))
            self.setPos(
                self.pos() + (move_dir * full_projection_list[-1]).toPointF())
            # print("pos after moving = " + str(self.pos()))

    def find_all_lines(self, item):

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

    def find_colliding_lines_and_dots(self, tested_list, second_list, item):
        lines_list = []
        dots_list = []
        point_of_intersection = QPointF()
        # find bounded lines
        for test_line in tested_list:
            # add instersection dots
            for second_line in second_list:
                intersection_type = test_line.intersect(
                    second_line, point_of_intersection)
                if (QLineF.BoundedIntersection == intersection_type and
                        test_line not in lines_list):
                    lines_list.append(QLineF(test_line))
                    # print("find_colliding_lines_and_dots::add new colliding line" +
                        # str(test_line))
        # find lines fully inside item:
        rect = QRectF(
            item.mapToScene(
                QPointF(
                    - item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2)),
            item.mapToScene(
                QPointF(
                    item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)))
        for test_line in tested_list:
            if (rect.contains(test_line.p1()) and
                rect.contains(test_line.p2()) and
                    test_line not in lines_list):
                lines_list.append(test_line)
                # print("find_colliding_lines_and_dots::add new line in rect" +
                    # str(test_line))


        if len(lines_list) > 1:
            for first in lines_list:
                for second in lines_list:
                    if first != second:
                        if (first.p1() == second.p1() or
                            first.p1() == second.p2() and
                                first.p1() not in dots_list):
                                dots_list.append(first.p1())
                                # print("find_colliding_lines_and_dots::add colliding dot")
                        if (first.p2() == second.p1() or
                            first.p2() == second.p2() and
                                first.p2() not in dots_list):
                                dots_list.append(first.p2())
                                # print("find_colliding_lines_and_dots::add colliding dot")

        return lines_list, dots_list

    def find_moving_vect(self, my_lines, obj_lines, item):
        all_dots_list = []
        point_of_intersection = QPointF()
        # find bounded lines
        for my_line in my_lines:
            # add instersection dots
            for obj_line in obj_lines:
                intersection_type = my_line.intersect(
                    obj_line, point_of_intersection)
                if QLineF.BoundedIntersection == intersection_type:
                    all_dots_list.append(QPointF(point_of_intersection))
        # find lines fully inside me:
        rect = QRectF(
            self.mapToScene(
                QPointF(
                    - self.boundingRect().width() / 2,
                    - self.boundingRect().height() / 2)),
            self.mapToScene(
                QPointF(
                    self.boundingRect().width() / 2,
                    self.boundingRect().height() / 2)))

        for obj_line in obj_lines:
            if (rect.contains(obj_line.p1()) and
                    rect.contains(obj_line.p2())):
                all_dots_list.append(obj_line.p1())
                all_dots_list.append(obj_line.p2())

        # sort list of dots
        all_dots_list = sorted(
            all_dots_list,
            key=lambda value: (QLineF(
                QPointF(0, 0),
                item.mapToItem(item, value)).angle()))

        normal_lines = []
        for idx_first, dot_first in enumerate(all_dots_list):
            for idx_second, dot_second in enumerate(all_dots_list):
                if (idx_first == idx_second + 1 or
                    (idx_first == len(all_dots_list) - 1 and
                        idx_second == 0)):
                    normal_lines.append(
                        QLineF(
                            dot_first,
                            dot_second).normalVector())

        normal_lines = sorted(
            normal_lines,
            key=lambda value: value.length())
        # print("move direction = " + str(
            # QVector2D(
                # normal_lines[-1].p2() - normal_lines[-1].p1()).normalized()))
        return QVector2D(
            normal_lines[-1].p2() - normal_lines[-1].p1()).normalized()

    def check_point_belongs_to_line(self, item_line, intersect_point):
        # y = kx + b
        # find k and b:
        # if x1 == x2 => line is x = number
        if item_line.x1() - item_line.x2() != 0:
            k = (
                (item_line.y1() - item_line.y2()) /
                (item_line.x1() - item_line.x2()))
            b = item_line.y1() - k * item_line.x1()
            if k * intersect_point.x() + b == intersect_point.y():
                return True
            else:
                return False
        else:
            if (
                item_line.x1() == intersect_point.x() and
                intersect_point.y() >= min(
                    item_line.y1(),
                    item_line.y2()) and
                intersect_point.y() <= max(
                    item_line.y1(),
                    item_line.y2())):
                return True
            else:
                return False
