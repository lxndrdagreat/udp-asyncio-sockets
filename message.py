from enum import Enum
import json

class MESSAGE_TYPE(Enum):
    HELLO = 1

def create_message(msg_type, package):
    msg = {
        "type": msg_type.value,
        "pkg": package
    }

    msg_json = json.dumps(msg)

    return bytes(msg_json+"\n", "utf-8")

def parse_message(message):
    parsed = message.decode("utf-8").rstrip()
    return json.loads(parsed)
