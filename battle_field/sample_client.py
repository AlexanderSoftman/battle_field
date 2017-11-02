import readchar
import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 7755

def main():
	print('for exit press "q"');
	print('for move pess: "w" "a" "s" "d"');
	print('for shut pess: " "');
	print('for create personage press: "r"');
	print('for delete personage press: "t"');

	sock = socket.socket(
		socket.AF_INET,
		socket.SOCK_DGRAM)
	c = 0
	_id = 0
	
	while c != 'q':
		c = readchar.readchar()
		if c == 'w':
			cmd = {'cmd':'increase_speed', 'data':{'id':_id}}
			sock.sendto(json.dumps(cmd).encode(), (UDP_IP, UDP_PORT))
			print(sock.recv(128).decode())
		elif c == 's':
			cmd = {'cmd':'reduce_speed', 'data':{'id':_id}}
			sock.sendto(json.dumps(cmd).encode(), (UDP_IP, UDP_PORT))
			print(sock.recv(128).decode())
		elif c == 'a':
			cmd = {'cmd':'reduce_angle', 'data':{'id':_id}}
			sock.sendto(json.dumps(cmd).encode(), (UDP_IP, UDP_PORT))
			print(sock.recv(128).decode())
		elif c == 'd':
			cmd = {'cmd':'increase_angle', 'data':{'id':_id}}
			sock.sendto(json.dumps(cmd).encode(), (UDP_IP, UDP_PORT))
			print(sock.recv(128).decode())
		elif c == ' ':
			cmd = {'cmd':'create_bullet', 'data':{'id':_id}}
			sock.sendto(json.dumps(cmd).encode(), (UDP_IP, UDP_PORT))
			print(sock.recv(128).decode())
		elif c == 'r':
			cmd = {'cmd':'create_personage', 'data':{'pos':[0, 0]}}
			sock.sendto(json.dumps(cmd).encode(), (UDP_IP, UDP_PORT))
			_id = json.loads(sock.recv(128).decode())['data']['id']
		elif c == 't':
			cmd = {'cmd':'delete_personage', 'data':{'id':_id}}
			sock.sendto(json.dumps(cmd).encode(), (UDP_IP, UDP_PORT))
			print(sock.recv(128).decode())

		# print('char:%s type:%s ' % (c, type(c)))

if __name__ == '__main__':
	main()