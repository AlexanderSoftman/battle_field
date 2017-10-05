from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import (QTimer, QTime, qrand, QPointF, QRectF)

from personage import Personage


class SceneWrapper(QGraphicsScene):

    pers_count_maximum = 10

    def __init__(self, *xxx, **kwargs):
        QGraphicsScene.__init__(self, *xxx, **kwargs)
        self.setSceneRect(-1000, -1000, 2000, 2000)
        self.setItemIndexMethod(QGraphicsScene.NoIndex)

        # create timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.dt = 1.0 / 30.0
        self.timer.start(self.dt * 1000)
        self.time = QTime()
        self.time.start()
        # self.addRect(QRectF(0, 0, 10, 10))
        # create initial objects
        for i in range(self.pers_count_maximum):
            pos_x = qrand() % 1000
            pos_y = qrand() % 1000
            pos = QPointF(pos_x, pos_y)
            angle = qrand() % 360
            self.addItem(Personage(self, pos, angle))


    # check by timer that we have enough tanks on battle
    def timerEvent(self):
        for item in self.items():
            item.update()
        if len(self.items()) < self.pers_count_maximum:
            pos_x = qrand() % 1000
            pos_y = qrand() % 1000
            pos = QPointF(pos_x, pos_y)
            angle = qrand() % 360
            self.addItem(Personage(self, pos, angle))
