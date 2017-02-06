# Non-asyncio threaded server
#
# Ctrl+C to kill
#
import socketserver
import socket
import threading
import json
from message import MessageProtocol

class ThreadedUDPEventServer(socketserver.ThreadingMixIn, socketserver.UDPServer):

    def __init__(self, server_address, bind_and_activate=True):
        """Constructor.  May be extended, do not override."""
        socketserver.UDPServer.__init__(self, server_address, None, bind_and_activate)

        self._message_protocol = MessageProtocol()

        # remember connected clients
        self.clients = []

        # event handlers
        self.handlers = {}

    def _trigger(self, event, data, addr):
        if event in self.handlers:
            self.handlers[event](data, addr)
        else:
            print("Unhandled event [{}]. Payload: {}".format(event, data))

    def finish_request(self, request, client_address):
        if client_address not in self.clients:            
            self.clients.append(client_address)
            self._trigger('connected', None, client_address)

        message_type, payload = self._message_protocol.parse(request[0])
        self._trigger(message_type, payload, client_address)

    def on(self, event, handler=None):
        def set_handler(handler):
            self.handlers[event] = handler
            return handler

        if handler is None:
            return set_handler
        set_handler(handler)

    def send(self, client, event, payload):
        msg = self._message_protocol.create(event, payload)
        self.socket.sendto(msg, client)

    def send_all(self, event, payload):
        for client in self.clients:
            self.send(client, event, payload)

server = ThreadedUDPEventServer(('localhost', 9999))

@server.on('connected')
def connected(msg, socket):
    print("New client: {}".format(socket))

@server.on('message')
def got_message(msg, socket):
    print("[{}]: {}".format(socket, msg))
    server.send_all('message', msg)

if __name__ == "__main__":
    
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    while True:
        pass

    server.shutdown()
