from PyQt5 import QtWidgets
from PyQt5 import QtCore
from battle_field.items import tank
from battle_field.items import obstacle
from battle_field import server
import logging

LOG = logging.getLogger(__name__)


class SceneWrapper(QtWidgets.QGraphicsScene):

    tank_bots_count_maximum = 2
    obstackles_count_maximum = 10
    safety_objects_distance = 100

    # define buttons

    up = 16777235
    down = 16777237
    left = 16777234
    right = 16777236
    space = 32
    cntrl = 16777249
    alt = 16777251

    tank_list = []
    # simple_tank_health = 100

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
        self.create_test_scene()
        self.server = server.Server(self)

        # create obstacle.Obstacles
        for i in range(self.obstackles_count_maximum):
            pos_x = -1000 + QtCore.qrand() % 2000
            pos_y = -1000 + QtCore.qrand() % 2000
            pos = QtCore.QPointF(pos_x, pos_y)
            # angle = 0
            self.addItem(obstacle.Obstacle(self, pos, 0))

        # debug only return
        return

        # create tanks objects (do not collide with obstackles!)
        # for i in range(self.pers_count_maximum):
        #     pos_x = QtCore.qrand() % 1000
        #     pos_y = QtCore.qrand() % 1000
        #     pos = QtCore.QPointF(pos_x, pos_y)
        #     angle = QtCore.qrand() % 360
        #     self.addItem(tank.Tank(
        #         self, pos, angle, self.simple_tank_health))
        self.my_tank = tank.Tank(
            self, QtCore.QPointF(500, -900), 0, False)
        self.addItem(self.my_tank)

        # generate obstacle.Obstacles at battle_field
        tanks_count_current = 0
        while (tanks_count_current < self.tank_bots_count_maximum):
            # generate random point
            pos_x = -1000 + QtCore.qrand() % 2000
            pos_y = -1000 + QtCore.qrand() % 2000
            pos = QtCore.QPointF(pos_x, pos_y)
            # angle = 0  # QtCore.qrand() % 360
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
                if (isinstance(item, tank.Tank) or
                        isinstance(item, obstacle.Obstacle)):
                    permission_flag = False
                    break
            if (permission_flag is True):
                self.addItem(self.tank_list[-1])
                tanks_count_current += 1

    # check by timer that we have enough tanks on battle
    def timerEvent(self):
        # check tank health:
        # for one_tank in self.tank_list:
            # if one_tank.health < 0:
                # self.scene().removeItem(one_tank.tank_body)
                # self.tank_list.remove(one_tank)
        for item in self.items():
            if (item is not None):
                item.update()
        if len(self.items()) < self.tank_bots_count_maximum:
            pos_x = -1000 + QtCore.qrand() % 2000
            pos_y = -1000 + QtCore.qrand() % 2000
            pos = QtCore.QPointF(pos_x, pos_y)
            angle = QtCore.qrand() % 360
            self.addItem(
                tank.Tank(
                    self, pos, angle))

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == self.left:
                self.my_tank.reduce_angle()
            elif event.key() == self.right:
                self.my_tank.increase_angle()
            elif event.key() == self.up:
                self.my_tank.increase_speed()
            elif event.key() == self.down:
                self.my_tank.reduce_speed()
            elif event.key() == self.cntrl:
                self.my_tank.tower.reduce_rotation_speed()
            elif event.key() == self.alt:
                self.my_tank.tower.increase_rotation_speed()
            elif event.key() == self.space:
                self.my_tank.tower.create_bullet()
            # print(event.key())
            return True
        else:
            return QtWidgets.QGraphicsScene.eventFilter(self, object, event)

    def create_test_scene(self):
        self.my_tank = tank.Tank(
            self, QtCore.QPointF(0, 0), 90, False)
        self.addItem(self.my_tank)
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
        # self.enemy_tank = tank.Tank(
            # self, QtCore.QPointF(700, 0), 180, True)
        # self.enemy_tank_2 = tank.Tank(
            # self, QtCore.QPointF(0, 180), 90, True)
        # self.addItem(self.enemy_tank)
        # self.addItem(self.enemy_tank_2)
