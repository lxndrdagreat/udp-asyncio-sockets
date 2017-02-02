# spammer.py
#
# This spams one message, over and over again, to a server.
#
# Ctrl+C to kill
#
import socket
import sys
import time
import json
from message import MESSAGE_TYPE, create_message

HOST, PORT = "localhost", 9999
data = {
    "type": "hello",
    "message": "hello world"
}

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
try:
    while True:
        sock.sendto(create_message(MESSAGE_TYPE.HELLO, "hello, world"), (HOST, PORT))
        # received = str(sock.recv(1024), "utf-8")

        print("Sent:     {}".format(data))
        # print("Received: {}".format(received))

        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:

    sock.close()