from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import (QTimer, QTime, qrand, QPointF, QRectF, QEvent)

from battle_field.items.personage import Personage
from battle_field.items.obstacle import Obstacle


class SceneWrapper(QGraphicsScene):

    pers_count_maximum = 0
    obstackles_count_maximum = 0
    safety_objects_distance = 100

    # define buttons
    up = 16777235
    down = 16777237
    left = 16777234
    right = 16777236
    space = 32
    cntrl = 16777249
    alt = 16777251

    def __init__(self, *xxx, **kwargs):
        QGraphicsScene.__init__(self, *xxx, **kwargs)
        # self.setSceneRect(-1000, -1000, 2000, 2000)
        self.setSceneRect(-500, -500, 1000, 1000)
        self.setItemIndexMethod(QGraphicsScene.NoIndex)

        # create timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.dt = 1.0 / 30.0
        self.timer.start(self.dt * 1000)
        self.time = QTime()
        self.time.start()
        # self.addRect(QRectF(0, 0, 10, 10))

        self.create_scene()

        # create obstacles
        for i in range(self.obstackles_count_maximum):
            pos_x = -1000 + qrand() % 2000
            pos_y = -1000 + qrand() % 2000
            pos = QPointF(pos_x, pos_y)
            angle = 0
            self.addItem(Obstacle(self, pos, 0))

        # create personages objects (do not collide with obstackles!)
        # for i in range(self.pers_count_maximum):
            # pos_x = qrand() % 1000
            # pos_y = qrand() % 1000
            # pos = QPointF(pos_x, pos_y)
            # angle = qrand() % 360
            # self.addItem(Personage(self, pos, angle))

        # self.my_personage = Personage(self, QPointF(500, -900), 0, False)
        # self.addItem(self.my_personage)

        # generate obstacles at battle_field
        pers_count_current = 0
        while (pers_count_current < self.pers_count_maximum):
            # generate random point
            pos_x = -1000 + qrand() % 2000
            pos_y = -1000 + qrand() % 2000
            pos = QPointF(pos_x, pos_y)
            angle = 0  # qrand() % 360
            # check that we don't collide with other tanks positions
            # and obstackles positions
            left_up_corner = QPointF(
                pos_x - self.safety_objects_distance,
                pos_y - self.safety_objects_distance)
            right_down_corner = QPointF(
                pos_x + self.safety_objects_distance,
                pos_y + self.safety_objects_distance)
            safety_rect = QRectF(left_up_corner, right_down_corner)
            permission_flag = True
            for item in self.items(safety_rect):
                if isinstance(item, Personage) or isinstance(item, Obstacle):
                    permission_flag = False
                    break
            if (permission_flag is True):
                self.addItem(Personage(self, pos, angle))
                pers_count_current += 1

    # check by timer that we have enough tanks on battle
    def timerEvent(self):
        for item in self.items():
            item.update()
        if len(self.items()) < self.pers_count_maximum:
            pos_x = -1000 + qrand() % 2000
            pos_y = -1000 + qrand() % 2000
            pos = QPointF(pos_x, pos_y)
            angle = qrand() % 360
            self.addItem(Personage(self, pos, angle))

    def eventFilter(self, object, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == self.left:
                self.my_personage.reduce_angle()
            elif event.key() == self.right:
                self.my_personage.increase_angle()
            elif event.key() == self.up:
                self.my_personage.increase_speed()
            elif event.key() == self.down:
                self.my_personage.reduce_speed()
            elif event.key() == self.cntrl:
                self.my_personage.tower.reduce_rotation_speed()
            elif event.key() == self.alt:
                self.my_personage.tower.increase_rotation_speed()
            elif event.key() == self.space:
                self.my_personage.tower.create_bullet()
            print(event.key())
            return True
        else:
            return QGraphicsScene.eventFilter(self, object, event)

    def create_scene(self):
        self.my_personage = Personage(self, QPointF(0, 0), 0, False)
        self.addItem(self.my_personage)
        obstacle_1 = Obstacle(self, QPointF(100, 10), 0)
        obstacle_2 = Obstacle(self, QPointF(330, -10), 0)
        obstacle_3 = Obstacle(self, QPointF(330, -100), 0)
        self.addItem(obstacle_1)
        self.addItem(obstacle_2)
        self.addItem(obstacle_3)
        obstacle_1.setVisible(True)
        obstacle_2.setVisible(True)
        obstacle_3.setVisible(True)
