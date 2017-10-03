
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsRectItem
from PyQt5.QtCore import (QTimer, qrand, QLineF, QPointF, QRectF)
from PyQt5.QtGui import QPolygonF, QPixmap

import math
from bullet import Bullet


class Personage(QGraphicsPixmapItem):

    tank_picture_path = '/home/afomin/projects/pyqt5/examples' \
        '/graphicsview/pokemons/images/tank_2.jpg'

    def __init__(self, scene, pos, angle):
        QGraphicsPixmapItem.__init__(self)
        self.setPos(pos)
        self.setRotation(angle)
        self.speed = 10
        self.setPixmap(QPixmap(self.tank_picture_path))
        print("self.boundingRect(): " + str(self.boundingRect()))
        self.setOffset(
            - self.boundingRect().width() / 2,
            - self.boundingRect().height() / 2)
        self.setScale(0.15)
        self.last_shoot_time = scene.time.elapsed()
        self.last_angle_time = scene.time.elapsed()
        self.shoot_period = 3000
        self.angle_period = 3000 + qrand() % 5000

    def update(self):
        self.change_pos()
        self.create_bullet()
        self.change_angle()

    def create_bullet(self):
        if self.scene().time.elapsed() - self.last_shoot_time > \
                self.shoot_period:
            bullet_x = self.boundingRect().width()
            bullet_y = 0
            self.scene().addItem(Bullet(
                self.scene(),
                self.mapToScene(QPointF(bullet_x, bullet_y)),
                self.rotation()))
            self.last_shoot_time = self.scene().time.elapsed()

    def change_angle(self):
        if self.scene().time.elapsed() - self.last_angle_time > \
                self.angle_period:
            self.last_angle_time = self.scene().time.elapsed()
            self.setRotation(qrand() % 360)

    def change_pos(self):
        x = self.pos().x() + self.speed * math.cos(
            self.rotation() * math.pi / 180.0) * self.scene().dt
        y = self.pos().y() + self.speed * math.sin(
            self.rotation() * math.pi / 180.0) * self.scene().dt
        self.setPos(x, y)
