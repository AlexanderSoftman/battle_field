import os
import math
from PyQt5.QtGui import (QPixmap)
from PyQt5.QtWidgets import QGraphicsPixmapItem
import battle_field
from battle_field.items import tank
from battle_field.items import obstacle


class Bullet(QGraphicsPixmapItem):
    bullet_picture_path = os.path.join(
        os.path.split(battle_field.__file__)[0], 'images/bullet.png')

    # bullet_power = 101
    basic_speed = 265

    # Create the bounding rectangle
    def __init__(self, scene, pos, angle, initial_speed):
        QGraphicsPixmapItem.__init__(self)
        # print(
        #     "bullet pos_x = " + str(pos.x()) + "pos_y = " +
        #     str(pos.y()) + " angle = " + str(angle))
        self.setPos(pos)
        self.setRotation(angle)
        self.speed = self.basic_speed + initial_speed
        self.setPixmap(QPixmap(self.bullet_picture_path))
        self.setOffset(
            - self.boundingRect().width() / 2,
            - self.boundingRect().height() / 2)
        self.setScale(0.025)

    def update(self):

        x = self.pos().x() + self.speed * math.cos(
            self.rotation() * math.pi / 180.0) * self.scene().dt
        y = self.pos().y() + self.speed * math.sin(
            self.rotation() * math.pi / 180.0) * self.scene().dt
        self.setPos(x, y)

        for item in self.scene().collidingItems(self):
            if isinstance(item, tank.Tank):
                self.scene().removeItem(item)
                # item.make_damage(self.bullet_power)
                self.scene().removeItem(self)
                break
            if isinstance(item, obstacle.Obstacle):
                self.scene().removeItem(self)
                break
