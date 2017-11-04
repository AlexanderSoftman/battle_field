from PyQt5 import QtNetwork, QtCore
import json
import logging
from battle_field.items import tank

LOG = logging.getLogger(__name__)


class Server(QtCore.QObject):
    port = 7777

    def __init__(self, scene):
        super(Server, self).__init__()
        self.scene = scene
        self.personages = {
            0: self.scene.my_tank} if hasattr(scene, 'my_tank') else {}
        self.personage_index = 1
        self.commands_map = {
            'create_personage': self.create_personage,
            'delete_personage': self.delete_personage,
            'increase_speed': self.increase_speed,
            'reduce_speed': self.reduce_speed,
            'reduce_angle': self.reduce_angle,
            'increase_angle': self.increase_angle,
            'reduce_rotation_speed': self.reduce_rotation_speed,
            'increase_rotation_speed': self.increase_rotation_speed,
            'create_bullet': self.create_bullet
        }
        print("create server: interface:0.0.0.0 port:%s" % (self.port, ))
        self.udp_socket = QtNetwork.QUdpSocket()
        self.udp_socket.bind(QtNetwork.QHostAddress.AnyIPv4, self.port)
        self.udp_socket.readyRead.connect(self.read_pending_datagrams)

    # @QtCore.pyqtSlot()
    def read_pending_datagrams(self):
        print('read_pending_datagrams')
        while (self.udp_socket.hasPendingDatagrams()):
            datagram = self.udp_socket.receiveDatagram()
            self.handle_request(datagram)

    def handle_request(self, datagram):
        try:
            data = json.loads(datagram.data().data().decode())
            handler = self.commands_map.get(data['cmd'], None)
            res = handler(data) if handler else\
                {'error': 'wrong cmd:%s' % (data['cmd'], )}
        except KeyError as e:
            res = {'error': 'KeyError:%s' % (e, )}
        except json.decoder.JSONDecodeError as e:
            res = {'error': 'JSONDecodeError:%s' % (e, )}
        self.udp_socket.writeDatagram(
            json.dumps(res).encode(),
            datagram.senderAddress(),
            datagram.senderPort())

    def create_personage(self, data):
        cur_tank = tank.Tank(
            self, QtCore.QPointF(
                data['data']['pos'][0],
                data['data']['pos'][1]),
            0,
            False)
        self.personages[self.personage_index] = cur_tank
        self.addItem(cur_tank)
        cur_id = self.personage_index
        self.personage_index += 1
        return {'data': {'id': cur_id}}

    def delete_personage(self, data):
        if data['data']['id'] not in self.personages\
                or data['data']['id'] == 0:
            return {'error': 'personage_not_exit'}
        self.removeItem(self.personages[data['data']['id']])
        del self.personages[data['data']['id']]
        return {}

    def increase_speed(self, data):
        if data['data']['id'] not in self.personages:
            return {'error': 'personage_not_exit'}
        self.personages[data['data']['id']].increase_speed()
        return {}

    def reduce_speed(self, data):
        if data['data']['id'] not in self.personages:
            return {'error': 'personage_not_exit'}
        self.personages[data['data']['id']].reduce_speed()
        return {}

    def reduce_angle(self, data):
        if data['data']['id'] not in self.personages:
            return {'error': 'personage_not_exit'}
        self.personages[data['data']['id']].reduce_angle()
        return {}

    def increase_angle(self, data):
        if data['data']['id'] not in self.personages:
            return {'error': 'personage_not_exit'}
        self.personages[data['data']['id']].increase_angle()
        return {}

    def reduce_rotation_speed(self, data):
        if data['data']['id'] not in self.personages:
            return {'error': 'personage_not_exit'}
        self.personages[data['data']['id']].reduce_rotation_speed()
        return {}

    def increase_rotation_speed(self, data):
        if data['data']['id'] not in self.personages:
            return {'error': 'personage_not_exit'}
        self.personages[data['data']['id']].increase_rotation_speed()
        return {}

    def create_bullet(self, data):
        if data['data']['id'] not in self.personages:
            return {'error': 'personage_not_exit'}
        self.personages[data['data']['id']].tower.create_bullet()
        return {}
