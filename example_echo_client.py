# example_echo_client.py
#
# This spams one message, over and over again, to a server.
# It also handles responses from the server.
#
# Ctrl+C to kill
#
import socket
import sys
import time
import json
from message import MessageProtocol

HOST, PORT = "localhost", 9999

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setblocking(False)

message_protocol = MessageProtocol()

count = 1

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
try:
    while True:
        data = message_protocol.create("hello", "hello, world {}".format(count))
        count += 1
        sock.sendto(data, (HOST, PORT))

        try:
            message, address = sock.recvfrom(8192)
            if message:
                print(message)
        except:
            pass

        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:

    sock.close()