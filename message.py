from enum import Enum, auto

class Message:
    class Type(Enum):
        FIRST = auto()
        SECOND = auto()
        THIRD = auto()

    def __init__(self, type, sender_name, elem):
        self.type = type
        self.sender_name = sender_name
        self.elem = elem
