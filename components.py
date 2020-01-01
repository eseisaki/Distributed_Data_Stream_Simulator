"""Distributed stream system architecture simulation classes.

The purpose of these classes is to collect detailed statistics
that are independent of the particular algorithm, and report
them in a standardized (and therefore auto-processable) manner."""

__docformat__ = 'reStructuredText'


class Channel:
    """Point-to-point or broadcast unidirectional channel.

       Channels are used to collect network statistics. Each channel counts
       the number of messages and the total mesage size (in bytes).


       :type src: host
       :param src: the one that sends the msg
       :type dst: host
       :param dst: the one that receives the msg
       :type msg: int
       :param msg: number of msgs sent by this channel
       :type bytes: int
       :param bytes: bytes sent by this channel
    """

    def __init__(self, src, dst):
        """
        creates the associated parameters of a channel object

        :param src: the one that sends the msg
        :param dst: the one that receives the msg
        """

        self.src = src  # source node
        self.dst = dst  # dest node
        self.msg = 0  # no of msg sent
        self.bytes = 0  # no of msg recv


if __name__ == "__main__":
    c = Channel()
