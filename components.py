"""Distributed stream system architecture simulation classes.

The purpose of these classes is to collect detailed statistics
that are independent of the particular algorithm, and report
them in a standardized (and therefore auto-processable) manner."""

__docformat__ = 'reStructuredText'

from msg_types import *


class Channel:
    """Point-to-point or broadcast unidirectional channel.

       Channels are used to collect network statistics. Each channel counts
       the number of messages and the total message size (in bytes).


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

    def send(self, msgtype: MsgType, msg):
        """
        src calls this proxy method in order to sent a msg
        :type msgtype: MsgType
        :param msgtype: constant custom types of msgs
        :param msg: the msg to sent
        :return: None
        """
        self.msg += 1
        self.bytes += msgtype.size_in_bytes(msg)

        self.dst.receive(self, msgtype, msg)  # call remote method to dst


class Host:
    """
    Hosts are used as nodes in the network.

    :type nid: int (key) :param nid: the unique id of a host
    :type peers: set :param peers: includes nids of all possible destinations
    :type recv_channels: dict :param recv_channels: a list of all recv channels
    :type send_channels: dict :param send_channels: a list of all recv channels
    :type handlers: dict :param handlers: a list of all handler methods
    """

    def __init__(self, nid):
        """
        creates a host object given an id

        :param nid: unique id of a host
        """
        self.nid = nid
        self.peers = set()
        self.recv_channels = {}
        self.send_channels = {}
        self.handlers = {}

    def connect(self, peer, recv_channel, send_channel):
        """
        creates a connection between the caller and its peer

        :param peer: host to connect with
        :param recv_channel: channel to receive msgs from peer
        :param send_channel: channel to send msgs from peer
        :return: None
        """
        self.peers.add(peer)
        self.recv_channels[peer] = recv_channel
        self.send_channels[peer] = send_channel

    def send(self, peer, msgtype, msg):
        """
        remote method that calls the 'channel.send' proxy method to send a msg

        :param peer: host to send msg
        :param msgtype: type of the msg
        :param msg: the msg to be sent
        :return: None
        """
        self.send_channels[peer].send(msgtype, msg)

    # TODO: create handler methods
    def receive(self, channel, msgtype, msg):
        """
        a method to receive a msg from the channel
        it is called by the 'channel.send()' proxy method

        :param channel: channel to receive the msg from
        :param msgtype: type of the msg
        :param msg: the msg to be received
        :return: None
        """
        self.handlers[msgtype](channel, msgtype, msg)

    def add_handler(self, msgtype, handler_func):
        """
        add in the handlers list a user_given function to implement on the host

        :param msgtype: type of msg
        :param handler_func: the given function
        :return: None
        """
        self.handlers[msgtype] = handler_func


# TODO:create unit tests
class StarNetwork:
    """
     A star network  contains nodes, a coordinator and  their connections.

    :type k: int
    :param k: the number of nodes in the network
    """

    def __init__(self, k, node_type=Host,
                 coord_type=Host, channel_type=Channel):
        """
        initialize a star network object

        :param k: the number of nodes in the network
        """
        self.k = k  # no of nodes
        self.node_type = node_type
        self.coord_type = coord_type
        self.channel_type = channel_type

        # create k node objects
        self.nodes = [node_type(i) for i in range(k)]
        # create coordinator object
        self.coord = coord_type(None)

        # set up channels
        for node in self.nodes:
            self.link(node, self.coord)

    def link(self, node, coord):
        """
        creates bidirectional connection between a node and the coordinator

        :param node: the node to connect with the coordinator
        :param coord: the coordinator of the network
        :return: None
        """
        uplink = self.channel_type(node, coord)
        dnlink = self.channel_type(coord, node)

        node.connect(coord, dnlink, uplink)
        coord.connect(node, uplink, dnlink)


if __name__ == "__main__":
    print("Let's begin this sucking project!")
