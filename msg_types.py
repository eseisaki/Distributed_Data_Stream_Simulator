"""
Define all possible different message types and a way to count their byte size.
"""
import sys


class MsgType:
    """
    Define basic message types and handle undefined message types
    """
    def __init__(self, msgtype):

        if msgtype == "char":
            self.__bytes = 1
        elif msgtype == "int":
            self.__bytes = 4
        elif msgtype == "long":
            self.__bytes = 8
        elif msgtype == "string":
            self.__bytes = "count"
        else:
            raise AttributeError()

    def size_in_bytes(self, msg):
        """
        Count the byte size of a given message

        :param msg: the message to be counted
        :return: the size of the message in bytes
        """
        if self.__bytes is not "count":
            return self.__bytes
        else:
            return len(msg.encode())
