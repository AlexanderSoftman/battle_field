from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap


class Obstacle(QGraphicsPixmapItem):

    obstacle_picture_path = './src/images/wall_2.png'

    def __init__(self, scene, pos, angle):
        QGraphicsPixmapItem.__init__(self)
        self.setPos(pos)
        self.setRotation(angle)
        print("new obstacle created, coordinates: " + str(
            self.pos().x()) + " " + str(self.pos().y()))
        self.setPixmap(QPixmap(self.obstacle_picture_path))
        self.setOffset(
            - self.boundingRect().width() / 2,
            - self.boundingRect().height() / 2)
        self.setScale(0.2)
