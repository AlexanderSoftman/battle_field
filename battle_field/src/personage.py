
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
        item_vect = QVector2D(item.pos())
        move_dir = my_vect - item_vect
        move_dir = move_dir.normalized()
        # 2. add projection of all dots to move_dir
        # (vector A * vector B)
        my_dots_info = self.get_direction_info(self, move_dir, item.pos())
        item_dots_info = self.get_direction_info(item, move_dir, item.pos())
        # 3. sort lists of tuples by projections
        # to move_dir vector
        my_dots_info = sorted(
            my_dots_info,
            key=lambda item: item)

        item_dots_info = sorted(
            item_dots_info,
            key=lambda item: item)

        # 4. find distance of moving
        distance = item_dots_info[-1] - my_dots_info[0]
        print("distance = " + str(distance))

        # 5. add new coordinate
        self.setPos((QVector2D(self.pos()) + move_dir * distance).toPointF())

    def get_direction_info(self, item, direction, center_global):
        # return list of projection point to direction
        # vector to point (from center_global point)
        # ----------------- x
        # |               |
        # |               |
        # -----------------
        # y
        item_vectors = []
        # top line
        vector_to_point = QVector2D((
            QPointF(
                item.mapToScene(
                    item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2))) -
            center_global)
        item_vectors.append(
            QVector2D.dotProduct(vector_to_point, direction))

        # right line
        vector_to_point = QVector2D(
            QPointF((
                item.mapToScene(
                    - item.boundingRect().width() / 2,
                    - item.boundingRect().height() / 2))) -
            center_global)
        item_vectors.append(
            QVector2D.dotProduct(vector_to_point, direction))

        # bottom line
        vector_to_point = QVector2D(
            QPointF((
                item.mapToScene(
                    - item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2))) -
            center_global)
        item_vectors.append(
            QVector2D.dotProduct(vector_to_point, direction))

        # left line
        vector_to_point = QVector2D(
            QPointF((
                item.mapToScene(
                    item.boundingRect().width() / 2,
                    item.boundingRect().height() / 2))) -
            center_global)
        item_vectors.append(
            QVector2D.dotProduct(vector_to_point, direction))

        return item_vectors
