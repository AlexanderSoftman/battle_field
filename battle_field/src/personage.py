
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsRectItem
from PyQt5.QtCore import qrand, QRectF, QLineF, QPointF
from PyQt5.QtGui import QPolygonF, QPixmap, QVector2D

import math

from tower import Tower
from obstacle import Obstacle

class Personage(QGraphicsPixmapItem):

    tank_picture_path = './src/images/tank.png'

    def __init__(self, scene, pos, angle):
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
        self.tower = Tower(scene, self)

    def update(self):
        self.change_pos()
        self.add_new_angle()
        self.change_angle()
        self.bump_check()

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
        # 0. move_dir predicted

        # 1. find move_dir as normalized vector between center of
        # item and my center
        my_vect = QVector2D(self.pos())
        print("my pos = " + str(self.pos()))
        item_vect = QVector2D(item.pos())
        print("item pos = " + str(item.pos()))
        move_dir = my_vect - item_vect
        print("move_dir before normalized:")
        print("move_dir: x = " + str(move_dir.x()))
        print("move_dir: y = " + str(move_dir.y()))

        move_dir = move_dir.normalized()

        print("move_dir: x = " + str(move_dir.x()))
        print("move_dir: y = " + str(move_dir.y()))

        # 2. add projection of all dots to move_dir
        # (vector A * vector B)
        my_dots_info = self.get_direction_info(self, move_dir)
        for dot in my_dots_info:
            print("my dots info: x = " + str(dot[0].x()))
            print("my dots info: y = " + str(dot[0].y()))
            print("my dotProduct: " + str(dot[1]))

        item_dots_info = self.get_direction_info(item, move_dir)
        for dot in item_dots_info:
            print("item dots info: x = " + str(dot[0].x()))
            print("item dots info: y = " + str(dot[0].y()))
            print("item dotProduct: " + str(dot[1]))

        # 3. sort lists of tuples by projections
        # to move_dir vector
        my_dots_info = sorted(
            my_dots_info,
            key=lambda item: item[1])

        print("my dots info after sorted")
        for dot in my_dots_info:
            print("my dots: x = " + str(dot[0].x()))
            print("my dots: y = " + str(dot[0].y()))
            print("my dotProduct: " + str(dot[1]))

        item_dots_info = sorted(
            item_dots_info,
            key=lambda item: item[1])

        print("item dots info after sorted")
        for dot in item_dots_info:
            print("item dots: x = " + str(dot[0].x()))
            print("item dots: y = " + str(dot[0].y()))
            print("item dotProduct: " + str(dot[1]))

        # 4. find distance of moving
        print(
            "my_dots_info[len(my_dots_info) - 1][1] = " +
            str(my_dots_info[len(my_dots_info) - 1][1]))
        print(
            "item_dots_info[0][1] = " +
            str(item_dots_info[0][1]))
        print(
            "item_dots_info[len(item_dots_info) - 1][1] = " +
            str(item_dots_info[len(item_dots_info) - 1][1]))
        print(
            "my_dots_info[0][1] = " +
            str(my_dots_info[0][1]))

        distance = min(
            math.fabs(
                my_dots_info[len(my_dots_info) - 1][1] -
                item_dots_info[0][1]),
            math.fabs(
                item_dots_info[len(item_dots_info) - 1][1] -
                my_dots_info[0][1]))

        print("distance = " + str(distance))

        # 5. add new coordinate
        self.setPos((QVector2D(self.pos()) + move_dir * distance).toPointF())
        print(
            "new pos = " + str(
                (QVector2D(self.pos()) + move_dir * distance).toPointF()))

    def get_direction_info(self, item, direction):
        # return list of tuples
        # (vector to point, fabs of projection point to direction)
        # ----------------- x
        # |               |
        # |               |
        # -----------------
        # y
        item_vectors = []
        # top line
        vector_to_point = QVector2D(
            QPointF(
                item.mapToScene(
                    item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2)))
        item_vectors.append((
            vector_to_point,
            QVector2D.dotProduct(vector_to_point, direction)))

        # right line
        vector_to_point = QVector2D(
            QPointF(
                item.mapToScene(
                    - item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2)))
        item_vectors.append((
            vector_to_point,
            QVector2D.dotProduct(vector_to_point, direction)))

        # bottom line
        vector_to_point = QVector2D(
            QPointF(
                item.mapToScene(
                    - item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)))
        item_vectors.append((
            vector_to_point,
            QVector2D.dotProduct(vector_to_point, direction)))

        # left line
        vector_to_point = QVector2D(
            QPointF(
                item.mapToScene(
                    item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2)))
        item_vectors.append((
            vector_to_point,
            QVector2D.dotProduct(vector_to_point, direction)))

        return item_vectors
