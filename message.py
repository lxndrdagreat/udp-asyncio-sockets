from enum import Enum
import json

class MESSAGE_TYPE(Enum):
    HELLO = 0

class MessageProtocol:

    def create(self, msg_type, package):
        msg_json = "{}{}\n".format(msg_type.value, json.dumps(package))
        return bytes(msg_json, "utf-8")

    def parse(self, message):
        parsed = message.decode("utf-8").rstrip()
        msg = {
            "type": int(parsed[0]),
            "pkg": json.loads(parsed[1:])
        }    
        return msg