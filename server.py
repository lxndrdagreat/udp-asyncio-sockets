# Non-asyncio threaded server
#
# Ctrl+C to kill
#
import socketserver
import socket
import threading

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        socket.sendto(data.upper(), self.client_address)


class ThreadedUDPEventServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

class ThreadedUDPServer():
    def __init__(self):
        # if no message protocol is set, then messages sent and received will be
        # handled as-is.
        self._message_protocol = None

        self._server = None

        # Host and Port
        self._address = ('localhost', 9999)

        self._request_handler = ThreadedUDPRequestHandler

    def start(self):

        self._server = ThreadedUDPEventServer(self._address, self._request_handler)

        with self._server:

            server_thread = threading.Thread(target=self._server.serve_forever)
            server_thread.daemon = True
            server_thread.start()

            while True:
                pass

            self._server.shutdown()

if __name__ == "__main__":
    server = ThreadedUDPServer()
    server.start()