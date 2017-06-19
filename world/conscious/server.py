import socketserver

from world.ev3controls import robots
from world.ev3controls.movements import stop

class MyCompanionTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    body= robots.MyCompanion()


    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        arguments=self.data.decode("utf-8").split(" ")
        action_result=self.body.react(*arguments)
        data="Action Result: {}".format(action_result)
        self.request.sendall(bytes(data + "\n", "utf-8"))


class MyTCPServer(socketserver.TCPServer):
    def server_close(self):
        self.socket.close()
        stop()


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = MyTCPServer((HOST, PORT), MyCompanionTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
