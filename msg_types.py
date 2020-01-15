"""
Define all possible different message types and a way to count their byte size.
"""
import sys


class MsgType:
    """
    Define basic message types and handle undefined message types
    """
    def __init__(self, msgtype):
        self.msgtype = msgtype

    def size_in_bytes(self, msg):
        """
        Count the byte size of a given message

        :param msg: the message to be counted
        :return: the size of the message in bytes
        """
        return sys.getsizeof(msg)
