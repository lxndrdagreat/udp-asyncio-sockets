import asyncio
import json
from message import MESSAGE_TYPE, parse_message

class EventProtocol:
    def connection_made(self, transport):
        print('start', transport)
        self.transport = transport

    def datagram_received(self, data, addr):
        if self.server:
            self.server.handle(data, addr)
        # self.transport.sendto(data, addr)

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print('stop', exc)

class EventServer:
    def __init__(self):
        self.handlers = {}

        loop = asyncio.get_event_loop()

        t = asyncio.Task(loop.create_datagram_endpoint(EventProtocol, local_addr=('localhost', 9999)))
        transport, prot = loop.run_until_complete(t)

        self.protocol = prot
        self.protocol.server = self

    def handle(self, data, addr):        
        data = parse_message(data)        
        print('PARSED:', data, addr)
        if data['type'] == MESSAGE_TYPE.HELLO.value:
            print("it is a HELLO!")
            self._trigger(MESSAGE_TYPE.HELLO, data['pkg'], addr)


    def _trigger(self, event, data, addr):
        if self.handlers[event]:
            self.handlers[event](data, addr)

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


async def wakeup():
    while True:
        await asyncio.sleep(1)

serv = EventServer()

@serv.on(MESSAGE_TYPE.HELLO)
def hello(data, client):
    print("I AM THE HANDLER! THIS IS MY DATA: {}".format(data))

if __name__ == '__main__':
    print("starting up..")

    loop = asyncio.get_event_loop()

    asyncio.async(wakeup())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    print("stop")

    loop.stop()