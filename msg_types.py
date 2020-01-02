"""
Define all possible different message types and a way to count their byte size.
"""
import sys


class MsgType:
    """
    Define all possible different msg types
    """
    def __init(self, msgtype):

        try:
            if msgtype == "char":
                self.__bytes = 1
            elif msgtype == "int":
                self.__bytes = 4
            elif msgtype == "long":
                self.__bytes = 8
            elif msgtype == "string":
                self.__bytes = "count"
            else:
                raise AttributeError('msgtype')
        except AttributeError:
            print("Wrong message type.")

    def size_in_bites(self, msg):
        if self.__bytes is not "count":
            return self.__bytes
        else:
            return len(msg.encode(msg))
