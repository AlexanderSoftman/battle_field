import os
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import battle_field


class Obstacle(QtWidgets.QGraphicsPixmapItem):
    obstacle_picture_path = os.path.join(
        os.path.split(battle_field.__file__)[0], 'images/wall.png')

    def __init__(self, scene, pos, angle):
        QtWidgets.QGraphicsPixmapItem.__init__(self)
        self.setPos(pos)
        self.setRotation(angle)
        self.setPixmap(QtGui.QPixmap(self.obstacle_picture_path))
        self.setOffset(
            - self.boundingRect().width() / 2,
            - self.boundingRect().height() / 2)
        self.setScale(0.2)
