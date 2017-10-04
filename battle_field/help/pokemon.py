import math

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtCore import (QRectF, qrand, QTimer, QPointF)
from PyQt5.QtGui import (QColor, QPixmap)
class Pokemon(QGraphicsPixmapItem):
    #boundary:
    pixmap_item = 0
    adjust = 0.5
    BoundingRect = QRectF(-20 - adjust, -22 - adjust, 40 + adjust, 83 + adjust)
    color =  QColor(qrand() % 256, qrand() % 256, qrand() % 256)

    def __init__(self, t_pixmap_item):
        pixmap_item = t_pixmap_item
        #self.angle = 0.0
        #self.speed = 0.0
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000 / 33)
        #self.setRotation(0)

    def timerEvent(self):

        #self.speed += (-50 + qrand() % 100)
        #self.angle = qrand() % 360

        #dx = math.sin(self.angle) * 10

        #self.setRotation(self.rotation() + dx)
        #self.setPos(self.mapToParent(0, -(3 + math.sin(self.speed) * 3)))

        #self.setOffset(QPointF((-50 + qrand() % 100),(-50 + qrand() % 100)))
        #print("x = " + str(self.offset().x()),"y = " + str(self.offset().y()))
        #print("speed = " + str(self.speed),"angle = " + str(self.angle))

        pixmap_item.setPos(QPointF((-50 + qrand() % 100),(-50 + qrand() % 100)))
    '''
    def boundingRect(self):
        return self.BoundingRect
    '''
    '''
    def paint(self, painter, option, widget):
        
        # Body.
        painter.setBrush(self.color)
        painter.drawEllipse(-10, -20, 20, 40)

        # Eyes.
        painter.drawEllipse(-10, -17, 8, 8)
        painter.drawEllipse(2, -17, 8, 8)

        # Nose.
        painter.drawEllipse(QRectF(-2, -22, 4, 4))

        # Pupils.
        painter.drawEllipse(QRectF(-8.0 + 0, -17, 4, 4))
        painter.drawEllipse(QRectF(4.0 + 0, -17, 4, 4))

        painter.drawEllipse(-17, -12, 16, 16)
        painter.drawEllipse(1, -12, 16, 16)
    '''
        