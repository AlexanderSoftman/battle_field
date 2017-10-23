
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsRectItem
from PyQt5.QtCore import qrand, QRectF, QLineF, QPointF
from PyQt5.QtGui import QPixmap, QVector2D

import math
import sys

from tower import Tower
from obstacle import Obstacle


class Personage(QGraphicsPixmapItem):

    tank_picture_path = './src/images/tank.png'

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
        move_dir = QVector2D(self.pos() - item.pos())
        move_dir = move_dir.normalized()

        # 1. find all lines
        my_all_lines = self.find_all_lines(self)
        item_all_lines = self.find_all_lines(item)

        # 2. find colliding lines and dots
        my_lines, my_dots = self.find_colliding_lines_and_dots(
            my_all_lines, item_all_lines, item)
        item_lines, item_dots = self.find_colliding_lines_and_dots(
            item_all_lines, my_all_lines, self)

        # 3. find move direction

        # 4. for every my and item dot inside other object
        # create projection
        full_projection_list = []

        for my_dot in my_dots:
            # create parallel line:
            par_line = QLineF(my_dot, my_dot + move_dir.toPointF())
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
                    dots_intersected.append(QPointF(dot_intersected))
            # all item lines checked.
            # create list of projections vectors from
            # my point to direction
            dot_products_for_my_dot = []
            for dot in dots_intersected:
                vector = QVector2D(
                    QPointF(
                        dot.x() - my_dot.x(),
                        dot.y() - my_dot.y()))
                dot_products_for_my_dot.append(
                    QVector2D.dotProduct(vector, move_dir))
            # sort all dot product list
            dot_products_for_my_dot = sorted(
                dot_products_for_my_dot,
                key=lambda value: value)
            # check that list is not empty,
            # get maximum value (-1 element)
            if len(dot_products_for_my_dot) > 0:
                full_projection_list.append(
                    dot_products_for_my_dot[-1])

        # for every item dots create list of collision with my lines
        for item_dot in item_dots:
            # create parallel line:
            par_line = QLineF(item_dot, item_dot + move_dir.toPointF())
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

        # 9. move to maximum value from projection list
        if len(full_projection_list) > 0:
            self.setPos(
                self.pos() + (move_dir * full_projection_list[-1]).toPointF())


    def get_direction_info(self, item, direction, center_global):
        # return list of projection points to direction
        # vector to point (from center_global point)
        # ----------------- x
        # |               |
        # |               |
        # -----------------
        # y
        item_vectors = []
        # right up
        vector_to_point = QVector2D((
            QPointF(
                item.mapToScene(
                    item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2))) -
            center_global)
        item_vectors.append(
            QVector2D.dotProduct(vector_to_point, direction))

        # right left
        vector_to_point = QVector2D(
            QPointF((
                item.mapToScene(
                    - item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2))) -
            center_global)
        item_vectors.append(
            QVector2D.dotProduct(vector_to_point, direction))

        # left down
        vector_to_point = QVector2D(
            QPointF((
                item.mapToScene(
                    - item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2))) -
            center_global)
        item_vectors.append(
            QVector2D.dotProduct(vector_to_point, direction))

        # right down
        vector_to_point = QVector2D(
            QPointF((
                item.mapToScene(
                    item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2))) -
            center_global)
        item_vectors.append(
            QVector2D.dotProduct(vector_to_point, direction))

        return item_vectors

    def find_direction_vector(self, item):

        # 0. find rect of item in scene coordinates:
        item_rect = QRectF(
            item.mapToScene(
                QPointF(
                    - item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2),
                QPointF(
                    item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)))

        # 1. find all lines of my and item in scene coordinates:
        my_lines = find_all_lines_of_item(self)
        item_lines = find_all_lines_of_item(item)

        # 2. find all points of my
        points_of_my = []
        points_of_my.append(
            item.mapToScene(
                QPointF(
                    item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)))
        points_of_my.append(
            item.mapToScene(
                QPointF(
                    item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2)))
        points_of_my.append(
            item.mapToScene(
                QPointF(
                    - item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2)))
        points_of_my.append(
            item.mapToScene(
                QPointF(
                    - item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)))

        # 3. find points of my inside item
        points_of_my_inside_item = []
        for point in points_of_my:
            if (item_rect.contains(point)):
                points_of_my_inside_item.append(item)

        # 4. find intersections of lines between me and item
        points_of_intersections = []
        point_of_intersection = QPointF()
        for my_line, item_line in zip(my_lines, item_lines):
            if (QLineF.BoundedIntersection ==
                    item_line.intersect(my_line, point_of_intersection)):
                points_of_intersections.append(point_of_intersection)

        # 5. find lines inside object
            # 5.1. we should join two lists togeather
            # 5.2. we should move them to system coordinates of item
            # 5.3. sort them by angle
            # 5.4. extracts points and get 2 from list.
            # each time we should check that they belongs to one line
            # If the belongs to one line -> create line between 2 points
            # 5.5. find normales vectors to these lines
            # 5.6. get summ for all vectors

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

        for part in parts_of_item:
            print("part len = " + str(part.length()))
        return parts_of_item

    def find_colliding_lines_and_dots(self, tested_list, second_list, item):
        lines_list = []
        dots_list = []
        point_of_intersection = QPointF()
        # find bounded lines
        for test_line in tested_list:
            #add instersection dots
            for second_line in second_list:
                intersection_type = test_line.intersect(
                    second_line, point_of_intersection)
                if (QLineF.BoundedIntersection == intersection_type and
                        test_line not in lines_list):
                    lines_list.append(QLineF(test_line))
                    print("add bounded line")

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
                print("add inside rect line")

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

    def find_dots_of_colliding_lines(self, dots_list, lines):
        result_list = []
        for dot in dots_list:
            for line in lines:
                if (
                    min(
                        line.pointAt(0).x(),
                        line.pointAt(1).x()) <=
                    dot.x() <=
                    max(
                        line.pointAt(0).x(),
                        line.pointAt(1).x())) and (
                    min(
                        line.pointAt(0).y(),
                        line.pointAt(1).y()) <=
                    dot.y() <=
                    max(
                        line.pointAt(0).y(),
                        line.pointAt(1).y())) and (
                        dot not in result_list):
                    result_list.append(dot)

        return result_list

    def find_dots_belongs_to_item(self, dots_list, item):
        result_list = []
        rect = QRectF(
            item.mapToScene(
                QPointF(
                    - item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2)),
            item.mapToScene(
                QPointF(
                    item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)))
        print("QRectF = " + str(rect))
        for dot in dots_list:
            if rect.contains(dot):
                result_list.append(dot)
        for one in result_list:
            print ("dot belong to list: " + str(one))
        return result_list
        #item_dots_x = []
        #item_dots_y = []

        #for item_dot in item_dots:
         #   item_dots_x.append(item_dot.x())
          #  item_dots_y.append(item_dot.y())

        #for dot in dots_list:
         #   if (
          #      min(item_dots_x) <
           #     dot.x() <
            #    max(item_dots_x) and
             #   min(item_dots_y) <
              #  dot.y() <
               # max(item_dots_y)
            #):
             #   result_list.append(dot)
            #if rect.contains(dot):
                #result_list.append(dot)
        #return result_list

    def find_all_dots(self, item):
        points_list = []
        points_list.append(
            item.mapToScene(
                QPointF(
                    item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)))
        points_list.append(
            item.mapToScene(
                QPointF(
                    item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2)))
        points_list.append(
            item.mapToScene(
                QPointF(
                    - item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2)))
        points_list.append(
            item.mapToScene(
                QPointF(
                    - item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)))
        return points_list

    def check_point_belongs_to_line(self, item_line, intersect_point):
        # y = kx + b
        # find k and b:
        k = (
            (item_line.y1() - item_line.y2()) /
            (item_line.x1() - item_line.x2()))
        b = item_line.y1() - k * item_line.x1()
        if k * intersect_point.x() + b == intersect_point.y():
            return True
        else:
            return False
