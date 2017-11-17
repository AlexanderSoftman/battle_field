from PyQt5 import QtWidgets
from PyQt5 import QtCore

from battle_field.items import tank
from battle_field.items import obstacle
from battle_field.items import path_creator
from PyQt5 import QtNetwork
import json
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

    port = 9999

    def __init__(self, *xxx, **kwargs):
        QtWidgets.QGraphicsScene.__init__(self, *xxx, **kwargs)
        self.setSceneRect(-1000, -1000, 2000, 2000)
        # small test scene
        # self.setSceneRect(-500, -500, 1000, 1000)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        self.path_creator = path_creator.PathCreator(self, [obstacle.Obstacle])
        # create timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.dt = 1.0 / 30.0
        self.timer.start(self.dt * 1000)
        self.time = QtCore.QTime()
        self.time.start()
        self.create_test_scene()
        self.init_server()

        # create obstacle.Obstacles
        for i in range(self.obstackles_count_maximum):
            pos_x = -1000 + QtCore.qrand() % 2000
            pos_y = -1000 + QtCore.qrand() % 2000
            pos = QtCore.QPointF(pos_x, pos_y)
            # angle = 0
            self.addItem(obstacle.Obstacle(self, pos, 0))


        # create tanks objects (do not collide with obstackles!)
        # for i in range(self.pers_count_maximum):
        #     pos_x = QtCore.qrand() % 1000
        #     pos_y = QtCore.qrand() % 1000
        #     pos = QtCore.QPointF(pos_x, pos_y)
        #     angle = QtCore.qrand() % 360
        #     self.addItem(tank.Tank(
        #         self, pos, angle, self.simple_tank_health))
        return
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

    def mousePressEvent(self, event):
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

    def init_server(self):
        print("init_server: interface:0.0.0.0 port:%s" % (self.port, ))
        self.udp_socket = QtNetwork.QUdpSocket()
        self.udp_socket.bind(QtNetwork.QHostAddress.AnyIPv4, self.port)
        self.udp_socket.readyRead.connect(self.read_pending_datagrams)

        self.personages = {0: self.my_tank} if hasattr(self, 'my_tank') else {}
        self.personage_index = 1

    def read_pending_datagrams(self):
        # print('read_pending_datagrams')
        while (self.udp_socket.hasPendingDatagrams()):
            datagram = self.udp_socket.receiveDatagram()
            self.handle_request(datagram)

    def handle_request(self, datagram):
        try:
            data = json.loads(datagram.data().data().decode())
            res = {}
            if data['cmd'] == 'create_personage':
                cur_tank = tank.Tank(
                    self, QtCore.QPointF(
                        data['data']['pos'][0],
                        data['data']['pos'][1]),
                    0,
                    False)
                self.personages[self.personage_index] = cur_tank
                self.addItem(cur_tank)
                res = {'data': {'id': self.personage_index}}
                self.personage_index += 1
            elif data['cmd'] == 'delete_personage':
                if data['data']['id'] not in self.personages\
                        or data['data']['id'] == 0:
                    res = {'error': 'personage_not_exit'}
                else:
                    self.removeItem(self.personages[data['data']['id']])
                    del self.personages[data['data']['id']]
            elif data['cmd'] == 'increase_speed':
                if data['data']['id'] not in self.personages:
                    res = {'error': 'personage_not_exit'}
                else:
                    self.personages[data['data']['id']].increase_speed()
            elif data['cmd'] == 'reduce_speed':
                if data['data']['id'] not in self.personages:
                    res = {'error': 'personage_not_exit'}
                else:
                    self.personages[data['data']['id']].reduce_speed()
            elif data['cmd'] == 'reduce_angle':
                if data['data']['id'] not in self.personages:
                    res = {'error': 'personage_not_exit'}
                else:
                    self.personages[data['data']['id']].reduce_angle()
            elif data['cmd'] == 'increase_angle':
                if data['data']['id'] not in self.personages:
                    res = {'error': 'personage_not_exit'}
                else:
                    self.personages[data['data']['id']].increase_angle()
            elif data['cmd'] == 'reduce_rotation_speed':
                if data['data']['id'] not in self.personages:
                    res = {'error': 'personage_not_exit'}
                else:
                    self.personages[data['data']['id']].reduce_rotation_speed()
            elif data['cmd'] == 'increase_rotation_speed':
                if data['data']['id'] not in self.personages:
                    res = {'error': 'personage_not_exit'}
                else:
                    self.personages[data['data'][
                        'id']].increase_rotation_speed()
            elif data['cmd'] == 'create_bullet':
                if data['data']['id'] not in self.personages:
                    res = {'error': 'personage_not_exit'}
                else:
                    self.personages[data['data']['id']].tower.create_bullet()

            self.udp_socket.writeDatagram(
                json.dumps(res).encode(),
                datagram.senderAddress(),
                datagram.senderPort())
        except json.decoder.JSONDecodeError as e:
            LOG.exception(e)
            self.udp_socket.writeDatagram(
                json.dumps({'error': str(e)}).encode(),
                datagram.senderAddress(),
                datagram.senderPort())

    # check by timer that we have enough tanks on battle
    def timerEvent(self):
        # check tank health:
        # for one_tank in self.tank_list:
            # if one_tank.health < 0:
                # self.scene().removeItem(one_tank.tank_body)
                # self.tank_list.remove(one_tank)
        for item in self.items():
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
            self, QtCore.QPointF(0, 0), 0, False)
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
        #self.enemy_tank = tank.Tank(
            #self, QtCore.QPointF(1, 1), 120, True)
        #self.addItem(self.enemy_tank)
