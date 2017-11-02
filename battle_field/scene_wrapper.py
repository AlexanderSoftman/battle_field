from PyQt5 import QtWidgets
from PyQt5 import QtCore

from battle_field.items import personage
from battle_field.items import obstacle
from PyQt5 import QtNetwork
import json
import logging 

LOG = logging.getLogger(__name__)

class SceneWrapper(QtWidgets.QGraphicsScene):

    pers_count_maximum = 0
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

    port = 7755

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

        self.init_server()

    def init_server(self):
        self.udp_socket = QtNetwork.QUdpSocket()
        self.udp_socket.bind(QtNetwork.QHostAddress.AnyIPv4, self.port);
        self.udp_socket.readyRead.connect(self.read_pending_datagrams)

        self.personages = {}
        self.personage_index = 0

    def read_pending_datagrams(self):
        print('read_pending_datagrams')
        while (self.udp_socket.hasPendingDatagrams()):
            datagram = self.udp_socket.receiveDatagram()
            self.handle_request(datagram);

    def handle_request(self, datagram):
        try:
            data = json.loads(datagram.data().data().decode())
            res = {}
            if data['cmd'] == 'create_personage':
                cur_personage = personage.Personage(
                    self, QtCore.QPointF(
                        data['data']['pos'][0],
                        data['data']['pos'][1]),
                    0, False)
                self.personages[self.personage_index] = cur_personage
                self.addItem(cur_personage)
                res = {'data':{'id': self.personage_index}}
                self.personage_index += 1
            elif data['cmd'] == 'delete_personage':
                if data['data']['id'] not in self.personages:
                    res = {'error':'personage_not_exit'}
                else:
                    self.removeItem(self.personages[data['data']['id']])
                    del self.personages[data['data']['id']]
            elif data['cmd'] == 'increase_speed':
                if data['data']['id'] not in self.personages:
                    res = {'error':'personage_not_exit'}
                else:
                    self.personages[data['data']['id']].increase_speed()
            elif data['cmd'] == 'reduce_speed':
                if data['data']['id'] not in self.personages:
                    res = {'error':'personage_not_exit'}
                else:
                    self.personages[data['data']['id']].reduce_speed()
            elif data['cmd'] == 'increase_speed':
                if data['data']['id'] not in self.personages:
                    res = {'error':'personage_not_exit'}
                else:
                    self.personages[data['data']['id']].increase_speed()
            elif data['cmd'] == 'reduce_angle':
                if data['data']['id'] not in self.personages:
                    res = {'error':'personage_not_exit'}
                else:
                    self.personages[data['data']['id']].reduce_angle()
            elif data['cmd'] == 'increase_angle':
                if data['data']['id'] not in self.personages:
                    res = {'error':'personage_not_exit'}
                else:
                    self.personages[data['data']['id']].increase_angle()
            elif data['cmd'] == 'reduce_rotation_speed':
                if data['data']['id'] not in self.personages:
                    res = {'error':'personage_not_exit'}
                else:
                    self.personages[data['data']['id']].reduce_rotation_speed()
            elif data['cmd'] == 'increase_rotation_speed':
                if data['data']['id'] not in self.personages:
                    res = {'error':'personage_not_exit'}
                else:
                    self.personages[data['data']['id']].increase_rotation_speed()
            elif data['cmd'] == 'create_bullet':
                if data['data']['id'] not in self.personages:
                    res = {'error':'personage_not_exit'}
                else:
                    self.personages[data['data']['id']].create_bullet()

            self.udp_socket.writeDatagram(json.dumps(res).encode(), datagram.senderAddress(), datagram.senderPort())
        except json.decoder.JSONDecodeError as e:
            LOG.exception(e)
            self.udp_socket.writeDatagram(
                json.dumps({'error':str(e)}).encode(),
                datagram.senderAddress(),
                datagram.senderPort())

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
            # print(event.key())
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
