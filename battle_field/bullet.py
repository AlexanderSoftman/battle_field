from PyQt5.QtGui import (QPixmap)
from PyQt5.QtWidgets import QGraphicsPixmapItem

import math


class Bullet(QGraphicsPixmapItem):

    bullet_picture_path = '/home/afomin/projects/pyqt5/examples' \
        '/graphicsview/pokemons/images/bullet.jpg'

    # Create the bounding rectangle
    def __init__(self, scene, pos, angle):
        QGraphicsPixmapItem.__init__(self)
        print(
            "bullet pos_x = " + str(pos.x()) + "pos_y = " +
            str(pos.y()) + " angle = " + str(angle))
        self.setPos(pos)
        self.setRotation(angle)
        self.speed = 20
        self.setPixmap(QPixmap(self.bullet_picture_path))
        self.setOffset(
            - self.boundingRect().width() / 2,
            - self.boundingRect().height() / 2)
        self.setScale(0.05)

    def update(self):
        x = self.pos().x() + self.speed * math.cos(
            self.rotation() * math.pi / 180.0) * self.scene().dt
        y = self.pos().y() + self.speed * math.sin(
            self.rotation() * math.pi / 180.0) * self.scene().dt
        self.setPos(x, y)

        for item in self.scene().collidingItems(self):
            self.scene().removeItem(item)
            self.scene().removeItem(self)
            break
