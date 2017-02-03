import asyncio
import json
from message import MESSAGE_TYPE, MessageProtocol

class EventProtocol:
    def connection_made(self, transport):
        self.transport = transport        

    def datagram_received(self, data, addr):
        if self.server:
            self.server.handle(data, addr)        

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print('stop', exc)

class EventServer:
    def __init__(self, message_protocol=MessageProtocol):
        self.handlers = {}

        # keep a collection of clients
        self._sockets = []

        loop = asyncio.get_event_loop()

        task = asyncio.Task(loop.create_datagram_endpoint(EventProtocol, local_addr=('localhost', 9999)))
        transport, prot = loop.run_until_complete(task)

        self._server = transport
        self._protocol = prot
        self._protocol.server = self

        self._message_protocol = MessageProtocol()

    def handle(self, data, addr):
        if addr not in self._sockets:
            self._sockets.append(addr)
            print("new client connection: {}".format(addr))

        data = self._message_protocol.parse(data)     
        self._trigger(data['type'], data['pkg'], addr)


    def _trigger(self, event, data, addr):
        if self.handlers[event]:
            self.handlers[event](data, addr)
        else:
            print("Unhandled event [{}]. Payload: {}".format(event, data))

    def send(self, addr, event_type, payload):
        message = self._message_protocol.create(event_type, payload)
        self._server.sendto(message, addr)

    def send_all(self, event_type, payload):
        for client in self._sockets:
            self.send(client, event_type, payload)

    def on(self, event, handler=None):
        """Register an event handler.
        :param event: The event name. It can be any string. The event names
                      ``'connect'``, ``'message'`` and ``'disconnect'`` are
                      reserved and should not be used.
        :param handler: The function that should be invoked to handle the
                        event. When this parameter is not given, the method
                        acts as a decorator for the handler function.
        :param namespace: The Socket.IO namespace for the event. If this
                          argument is omitted the handler is associated with
                          the default namespace.
        Example usage::
            # as a decorator:
            @socket_io.on('connect', namespace='/chat')
            def connect_handler(sid, environ):
                print('Connection request')
                if environ['REMOTE_ADDR'] in blacklisted:
                    return False  # reject
            # as a method:
            def message_handler(sid, msg):
                print('Received message: ', msg)
                eio.send(sid, 'response')
            socket_io.on('message', namespace='/chat', message_handler)
        The handler function receives the ``sid`` (session ID) for the
        client as first argument. The ``'connect'`` event handler receives the
        WSGI environment as a second argument, and can return ``False`` to
        reject the connection. The ``'message'`` handler and handlers for
        custom event names receive the message payload as a second argument.
        Any values returned from a message handler will be passed to the
        client's acknowledgement callback function if it exists. The
        ``'disconnect'`` handler does not take a second argument.
        """

        def set_handler(handler):
            self.handlers[event] = handler
            return handler

        if handler is None:
            return set_handler
        set_handler(handler)
