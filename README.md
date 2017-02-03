# udp-asyncio-sockets
A messy attempt at building a UDP socket server with Python asyncio.

# Example

Run `example_echo_server.py` and `example_echo_client.py` to see it in action.

# Usage

## EventServer

## EventProtocol

## MessageProtocol

The `EventServer` uses a `MessageProtocol` class to handle translating messages
to and from byte data. The default and included `MessageProtocol` class turns
data into a message made up of identifier and payload.

You can create your own message handling by inheriting from `MessageProtocol` and
telling the `EventServer` to use it when you create it:

```
server = EventServer(MyCustomProtocol)
```
