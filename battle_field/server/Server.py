import socketserver
import json


class Server(socketserver.UDPServer):

    class MyUDPHandler(socketserver.BaseRequestHandler):
        def handle(self):
            scene = self.server.scene
            switch json.loads(self.request[0].decode())
            # data = json.loads(self.request[0].decode())
            # socket = self.request[1]
            # print ("{} wrote:".format(self.client_address[0]))
            # print (data)
            # socket.sendto(json.dumps(data).encode(), self.client_address)

    def __init__(self, scene, *args, **kwargs):
        socketserver.UDPServer.__init__(self, *args, **kwargs)
        self.scene = scene


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    scene = 1
    server = Server(scene, (HOST, PORT), Server.MyUDPHandler)
    server.serve_forever()
