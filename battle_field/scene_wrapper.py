from PyQt5 import QtWidgets
from PyQt5 import QtCore

from battle_field.items import personage
from battle_field.items import obstacle


class SceneWrapper(QtWidgets.QGraphicsScene):

    pers_count_maximum = 10
    obstackles_count_maximum = 20
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
        QtWidgets.QGraphicsScene.__init__(self, *xxx, **kwargs)
        self.setSceneRect(-1000, -1000, 2000, 2000)
        # small test scene
        # self.setSceneRect(-500, -500, 1000, 1000)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        # create timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.dt = 1.0 / 30.0
        self.timer.start(self.dt * 1000)
        self.time = QtCore.QTime()
        self.time.start()
        # self.create_test_scene()

        # create obstacle.Obstacles
        for i in range(self.obstackles_count_maximum):
            pos_x = -1000 + QtCore.qrand() % 2000
            pos_y = -1000 + QtCore.qrand() % 2000
            pos = QtCore.QPointF(pos_x, pos_y)
            angle = 0
            self.addItem(obstacle.Obstacle(self, pos, 0))

        # create personage.Personages objects (do not collide with obstackles!)
        for i in range(self.pers_count_maximum):
            pos_x = QtCore.qrand() % 1000
            pos_y = QtCore.qrand() % 1000
            pos = QtCore.QPointF(pos_x, pos_y)
            angle = QtCore.qrand() % 360
            self.addItem(personage.Personage(self, pos, angle))

        self.my_personage = personage.Personage(
            self, QtCore.QPointF(500, -900), 0, False)
        self.addItem(self.my_personage)

        # generate obstacle.Obstacles at battle_field
        pers_count_current = 0
        while (pers_count_current < self.pers_count_maximum):
            # generate random point
            pos_x = -1000 + QtCore.qrand() % 2000
            pos_y = -1000 + QtCore.qrand() % 2000
            pos = QtCore.QPointF(pos_x, pos_y)
            angle = 0  # QtCore.qrand() % 360
            # check that we don't collide with other tanks positions
            # and obstackles positions
            left_up_corner = QtCore.QPointF(
                pos_x - self.safety_objects_distance,
                pos_y - self.safety_objects_distance)
            right_down_corner = QtCore.QPointF(
                pos_x + self.safety_objects_distance,
                pos_y + self.safety_objects_distance)
            safety_rect = QtCore.QRectF(left_up_corner, right_down_corner)
            permission_flag = True
            for item in self.items(safety_rect):
                if (isinstance(item, personage.Personage) or
                        isinstance(item, obstacle.Obstacle)):
                    permission_flag = False
                    break
            if (permission_flag is True):
                self.addItem(personage.Personage(self, pos, angle))
                pers_count_current += 1

    # check by timer that we have enough tanks on battle
    def timerEvent(self):
        for item in self.items():
            item.update()
        if len(self.items()) < self.pers_count_maximum:
            pos_x = -1000 + QtCore.qrand() % 2000
            pos_y = -1000 + QtCore.qrand() % 2000
            pos = QtCore.QPointF(pos_x, pos_y)
            angle = QtCore.qrand() % 360
            self.addItem(personage.Personage(self, pos, angle))

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.KeyPress:
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
            return QtWidgets.QGraphicsScene.eventFilter(self, object, event)

    def create_test_scene(self):
        self.my_personage = personage.Personage(
            self, QtCore.QPointF(0, 0), 0, False)
        self.addItem(self.my_personage)
        Obstacle_1 = obstacle.Obstacle(
            self, QtCore.QPointF(100, 10), 0)
        Obstacle_2 = obstacle.Obstacle(
            self, QtCore.QPointF(330, -10), 0)
        Obstacle_3 = obstacle.Obstacle(
            self, QtCore.QPointF(330, -100), 0)
        self.addItem(Obstacle_1)
        self.addItem(Obstacle_2)
        self.addItem(Obstacle_3)
        Obstacle_1.setVisible(True)
        Obstacle_2.setVisible(True)
        Obstacle_3.setVisible(True)
