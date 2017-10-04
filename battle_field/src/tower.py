from PyQt5.QtCore import qrand, QPointF
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QPolygonF

import math

from bullet import Bullet


class Tower(QGraphicsPixmapItem):

    tower_picture_path = './src/images/head.png'

    def __init__(self, scene, parent):
        super(Tower, self).__init__(parent)
        print("new tower created, coordinates: " + str(self.pos().x()) + " " + str(self.pos().y()))
        self.rotation_speed = 30
        self.setPixmap(QPixmap(self.tower_picture_path))
        self.setOffset(
            - self.boundingRect().width() / 2,
            - self.boundingRect().height() / 2)
        self.setScale(0.9)
        self.last_shoot_time = scene.time.elapsed()
        self.last_angle_time = scene.time.elapsed()
        self.shoot_period = 7000
        self.angle_period = 7000
        self.destination_angle = self.rotation()
        #self.target = None

    def update(self):
        self.add_new_angle()
        self.change_angle()
        self.create_bullet()

    def create_bullet(self):
        if self.scene().time.elapsed() - self.last_shoot_time > \
                self.shoot_period:
            bullet_x = self.boundingRect().width()
            bullet_y = 0
            self.scene().addItem(Bullet(
                self.scene(),
                self.mapToScene(QPointF(bullet_x, bullet_y)),
                self.parentItem().rotation() + self.rotation()))
            self.last_shoot_time = self.scene().time.elapsed()

    def add_new_angle(self):
        if self.scene().time.elapsed() - self.last_angle_time > \
                self.angle_period:
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
                sign * self.rotation_speed * self.scene().dt
            )

    def scanning(self):
        # find new destination angle
        if self.scene().time.elapsed() - self.last_angle_time > \
                self.body_angle_period:
            self.last_angle_time = self.scene().time.elapsed()
            self.angle_period = -45 + (qrand() % 90)
        # go to destination angle
        if (self.rotation() != self.destination_body_angle):
            if (self.destination_body_angle - self.rotation() > 0):
                sign = 1
            else:
                sign = -1
            self.setRotation(
                self.rotation() +
                sign * self.body_rotation_speed * self.scene().dt
            )


    def search_and_destroy(self):

        enemy_tanks = self.scene().items(
            QPolygonF([
                self.mapToScene(0, 0),
                self.mapToScene(
                    (self.boundingRect().widght() *
                        math.cos(self.head_angle) * 10),
                    (- self.boundingRect().height() *
                        math.sin(self.head_angle)) * 10),
                self.mapToScene(
                    (self.boundingRect().widght() *
                        math.cos(self.head_angle) * 10),
                    (self.boundingRect().height() *
                        math.sin(self.head_angle)) * 10)]))
        for tank in enemy_tanks:
            if (isinstance(tank, Tower)):
                if tank is self:
                    continue
                self.target = tank
                break
        #else:
