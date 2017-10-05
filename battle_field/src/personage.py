
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsRectItem
from PyQt5.QtCore import qrand, QRectF
from PyQt5.QtGui import QPolygonF, QPixmap

import math

from tower import Tower


class Personage(QGraphicsPixmapItem):

    tank_picture_path = './src/images/tank.png'

    def __init__(self, scene, pos, angle):
        QGraphicsPixmapItem.__init__(self)
        self.rect = QGraphicsRectItem(QRectF(0, 0, 10, 10), self)
        self.setPos(pos)
        self.setRotation(angle)
        print("new tank created, coordinates: " + str(self.pos().x()) + " " + str(self.pos().y()))
        self.speed = 0
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
        # self.change_angle()

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
