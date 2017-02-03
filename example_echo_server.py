from event_server import EventServer
from message import MESSAGE_TYPE
import asyncio

async def wakeup():
    while True:
        await asyncio.sleep(1)

serv = EventServer()

@serv.on(MESSAGE_TYPE.HELLO.value)
def hello(data, client):
    print("[{}]: {}".format(client, data))
    # take the message from the client and send it right back.
    # serv.send(client, MESSAGE_TYPE.HELLO, "{}: {}".format(client, data))
    serv.send_all(MESSAGE_TYPE.HELLO, "{}: {}".format(client, data))


if __name__ == '__main__':
    print("starting up...")

    loop = asyncio.get_event_loop()

    asyncio.async(wakeup())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    print("stopping")

    loop.stop()