from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtNetwork
import enum
import json
import logging

from battle_field.items import obstacle
from battle_field.common import path_creator

from battle_field.items.vehicles.tank import tank
from battle_field.items.vehicles import four_wheels
from battle_field.items.vehicles import articulated
from battle_field.items.vehicles import cart


LOG = logging.getLogger(__name__)


class User(enum.Enum):
    TANK = 1
    FRONT_DRIVING_FOUR_WHEELS = 2
    ARTICULATED_FOUR_WHEELS = 3
    CART = 4


class SceneWrapper(QtWidgets.QGraphicsScene):

    # choose one of this guys
    # TANK
    # FRONT_DRIVING_FOUR_WHEELS
    # ARTICULATED_FOUR_WHEELS
    # CART
    user = User.TANK

    update_freq = 30.0

    tank_bots_count_maximum = 2
    obstackles_count_maximum = 10
    safety_objects_distance = 100

    # define buttons
    buttons = {
        'up': 16777235,
        'down': 16777237,
        'left': 16777234,
        'right': 16777236,
        'space': 32,
        'cntrl': 16777249,
        'alt': 16777251,
        'q': 81,
        'w': 87,
        'e': 69,
        'a': 65,
        's': 83,
        'd': 68
    }
    tank_list = []
    # simple_tank_health = 100

    port = 9999

    def __init__(self, isw, *xxx, **kwargs):
        QtWidgets.QGraphicsScene.__init__(self, *xxx, **kwargs)
        self.isw = isw
        self.setSceneRect(-1000, -1000, 2000, 2000)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        self.path_creator = path_creator.PathCreator(self, [obstacle.Obstacle])
        # create timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.dt = 1.0 / self.update_freq
        self.timer.start(self.dt * 1000)
        self.time = QtCore.QTime()
        self.time.start()
        self.create_user()
        self.create_field()
        # self.create_enemies()
        # self.init_server()

    def mousePressEvent(self, event):
        # turn off path creating while debug
        return
        bounders = [
            QtCore.QLineF(
                self.my_tank.mapToScene(
                    QtCore.QPointF(
                        self.my_tank.boundingRect().width() / 2,
                        0)),
                self.my_tank.mapToScene(
                    QtCore.QPointF(
                        0, 0))).length(),
            QtCore.QLineF(
                self.my_tank.mapToScene(
                    QtCore.QPointF(
                        self.my_tank.boundingRect().height() / 2,
                        0)),
                self.my_tank.mapToScene(
                    QtCore.QPointF(
                        0, 0))).length()]
        bounder_maximum = max(bounders[0], bounders[1])
        self.path_creator.create_li_shapes_tree(
            bounder_maximum,
            self.my_tank.pos(),
            event.scenePos())

    # check by timer that we have enough tanks on battle
    def timerEvent(self):
        for item in self.items():
            item.update()
        self.isw.update()
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
            if event.key() == self.buttons["left"]:
                if isinstance(self.my_vehicle, tank.Tank):
                    self.my_vehicle.reduce_angle()
                elif isinstance(
                    self.my_vehicle,
                        four_wheels.FourWheels):
                    self.my_vehicle.reduce_wa()
                elif isinstance(
                    self.my_vehicle,
                        articulated.Articulated):
                    self.my_vehicle.reduce_angle()
            elif event.key() == self.buttons["right"]:
                if isinstance(self.my_vehicle, tank.Tank):
                    self.my_vehicle.increase_angle()
                elif isinstance(
                    self.my_vehicle,
                        four_wheels.FourWheels):
                    self.my_vehicle.increase_wa()
                elif isinstance(
                    self.my_vehicle,
                        articulated.Articulated):
                    self.my_vehicle.increase_angle()
            elif event.key() == self.buttons["up"]:
                if isinstance(self.my_vehicle, tank.Tank):
                    self.my_vehicle.increase_speed()
                elif isinstance(
                    self.my_vehicle,
                        four_wheels.FourWheels):
                    self.my_vehicle.increase_wheels_speed()
                elif isinstance(
                    self.my_vehicle,
                        articulated.Articulated):
                    self.my_vehicle.increase_wheels_speed()
            elif event.key() == self.buttons["down"]:
                if isinstance(self.my_vehicle, tank.Tank):
                    self.my_vehicle.reduce_speed()
                elif isinstance(
                    self.my_vehicle,
                        four_wheels.FourWheels):
                    self.my_vehicle.reduce_wheels_speed()
                elif isinstance(
                    self.my_vehicle,
                        articulated.Articulated):
                    self.my_vehicle.reduce_wheels_speed()
            elif event.key() == self.buttons["cntrl"]:
                if isinstance(self.my_vehicle, tank.Tank):
                    self.my_vehicle.tower.reduce_rotation_speed()
            elif event.key() == self.buttons["alt"]:
                if isinstance(self.my_vehicle, tank.Tank):
                    self.my_vehicle.tower.increase_rotation_speed()
            elif event.key() == self.buttons["space"]:
                if isinstance(self.my_vehicle, tank.Tank):
                    self.my_vehicle.tower.create_bullet()
            elif event.key() == self.buttons["q"]:
                if isinstance(self.my_vehicle, cart.Cart):
                    self.my_vehicle.increase_left_ws()
            elif event.key() == self.buttons["a"]:
                if isinstance(self.my_vehicle, cart.Cart):
                    self.my_vehicle.reduce_left_ws()
            elif event.key() == self.buttons["e"]:
                if isinstance(self.my_vehicle, cart.Cart):
                    self.my_vehicle.increase_right_ws()
            elif event.key() == self.buttons["d"]:
                if isinstance(self.my_vehicle, cart.Cart):
                    self.my_vehicle.reduce_right_ws()
            # LOG.debug("pressed button: %s" % (event.key(), ))
            return True
        else:
            return QtWidgets.QGraphicsScene.eventFilter(self, object, event)

    def create_user(self):
        if self.user == User.ARTICULATED_FOUR_WHEELS:
            self.my_vehicle = articulated.Articulated(
                scene=self,
                frame_length={
                    "back": 50,
                    "front": 30},
                init_pos={
                    "position": QtCore.QPointF(0, 0),
                    "heading": 0},
                wheel_size={
                    "breadth": 5,
                    "diameter": 20})
        elif self.user == User.FRONT_DRIVING_FOUR_WHEELS:
            self.my_vehicle = four_wheels.FourWheels(
                self,
                body_size={
                    "width": 100,
                    "height": 50
                },
                init_pos={
                    "position": QtCore.QPointF(0, 0),
                    "heading": -45
                },
                wheel_size={
                    "breadth": 10,
                    "diameter": 30
                })
        elif self.user == User.TANK:
            self.my_vehicle = tank.Tank(
                self, QtCore.QPointF(-100, 0), 0, False)
        elif self.user == User.CART:
            body_size = {
                "x": 100,
                "y": 50
            }
            wheel_size = {
                "breadth": 5,
                "diameter": 20
            }
            init_pos = {
                "position": QtCore.QPointF(0, 0),
                "heading": 0
            }
            self.my_vehicle = cart.Cart(
                self,
                self.update_freq,
                self.isw.callbacks,
                False,
                body_size=body_size,
                init_pos=init_pos,
                wheel_size=wheel_size)
            # create duplication on isw
            self.isw.vehicle = cart.Cart(
                self.isw,
                self.update_freq,
                None,
                False,
                body_size=body_size,
                init_pos=init_pos,
                wheel_size=wheel_size)
            self.isw.addItem(self.isw.vehicle)
        self.addItem(self.my_vehicle)

    def create_field(self):
        # simple field
        # self.enemy_tank = tank.Tank(
            # self, QtCore.QPointF(700, 0), 180, True)
        # self.enemy_tank_2 = tank.Tank(
            # self, QtCore.QPointF(0, 180), 90, True)
        # self.addItem(self.enemy_tank)
        # self.addItem(self.enemy_tank_2)
        # return
        # create obstacle.Obstacles
        for i in range(self.obstackles_count_maximum):
            pos_x = -1000 + QtCore.qrand() % 2000
            pos_y = -1000 + QtCore.qrand() % 2000
            pos = QtCore.QPointF(pos_x, pos_y)
            # angle = 0
            self.addItem(obstacle.Obstacle(self, pos, 0))

    def create_enemies(self):
        # just one enemy
        self.enemy_tank = tank.Tank(
            self, QtCore.QPointF(1, 1), 120, True)
        self.addItem(self.enemy_tank)

        return
        # a lot of enemies
        # generate obstacle.Obstacles at battle_field
        tanks_count_current = 0
        while (tanks_count_current < self.tank_bots_count_maximum):
            # generate random point
            pos_x = -1000 + QtCore.qrand() % 2000
            pos_y = -1000 + QtCore.qrand() % 2000
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
