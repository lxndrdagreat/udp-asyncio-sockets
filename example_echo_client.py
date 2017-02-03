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
from message import MESSAGE_TYPE, MessageProtocol

HOST, PORT = "localhost", 9999

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message_protocol = MessageProtocol()

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
try:
    while True:
        data = message_protocol.create(MESSAGE_TYPE.HELLO, "hello, world")
        sock.sendto(data, (HOST, PORT))
        received = sock.recv(1024)
        received = message_protocol.parse(received)

        print("Sent:     {}".format(data))
        print("Received: {}".format(received))

        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:

    sock.close()