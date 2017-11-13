import readchar
import socket
import json
import logging
from battle_field import scene_wrapper
LOG = logging.getLogger(__name__)

UDP_IP = "127.0.0.1"
UDP_PORT = scene_wrapper.SceneWrapper.port


def main():
    print('for exit press "q"')
    print('for move pess: "w" "a" "s" "d"')
    print('for shut pess: " "')
    print('for create personage press: "r"')
    print('for delete personage press: "t"')

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM)
    sock.settimeout(0.5)
    char = 0
    _id = 0

    while char != 'q':
        try:
            char = readchar.readchar()
            if char == 'w':
                cmd = {'cmd': 'increase_speed', 'data': {'id': _id}}
                sock.sendto(json.dumps(cmd).encode(), (UDP_IP, UDP_PORT))
                sock.recv(128).decode()
            elif char == 's':
                cmd = {'cmd': 'reduce_speed', 'data': {'id': _id}}
                sock.sendto(json.dumps(cmd).encode(), (UDP_IP, UDP_PORT))
                sock.recv(128).decode()
            elif char == 'a':
                cmd = {'cmd': 'reduce_angle', 'data': {'id': _id}}
                sock.sendto(json.dumps(cmd).encode(), (UDP_IP, UDP_PORT))
                sock.recv(128).decode()
            elif char == 'd':
                cmd = {'cmd': 'increase_angle', 'data': {'id': _id}}
                sock.sendto(json.dumps(cmd).encode(), (UDP_IP, UDP_PORT))
                sock.recv(128).decode()
            elif char == ' ':
                cmd = {'cmd': 'create_bullet', 'data': {'id': _id}}
                sock.sendto(json.dumps(cmd).encode(), (UDP_IP, UDP_PORT))
                sock.recv(128).decode()
            elif char == 'r':
                cmd = {'cmd': 'create_personage', 'data': {'pos': [0, 0]}}
                sock.sendto(json.dumps(cmd).encode(), (UDP_IP, UDP_PORT))
                _id = json.loads(sock.recv(128).decode())['data']['id']
            elif char == 't':
                cmd = {'cmd': 'delete_personage', 'data': {'id': _id}}
                sock.sendto(json.dumps(cmd).encode(), (UDP_IP, UDP_PORT))
                sock.recv(128).decode()
            # print('char:%s type:%s ' % (char, type(char)))
        except socket.timeout as e:
            LOG.warning('socket error:%s' % (e,))


if __name__ == '__main__':
    main()
