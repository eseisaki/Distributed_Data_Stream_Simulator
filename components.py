"""Distributed stream system architecture simulation classes.

The purpose of these classes is to collect detailed statistics
that are independent of the particular algorithm, and report
them in a standardized (and therefore auto-processable) manner."""

__docformat__ = 'reStructuredText'

import sys


# -----------------------------------------------------------------------------
#
#   Channels
#
# -----------------------------------------------------------------------------

class Channel:
    """Point-to-point or broadcast unidirectional channel.

       Channels are used to collect network statistics. Each channel counts
       the number of messages and the total message size (in bytes).

       Message types are defined by a "string" same as the name of the
       endpoint.

       Each endpoint is associated with a request channel, and --if it is not
       one-way--- with a response channel.


       :type src: host
       :param src: the one that sends the msg
       :type dst: host
       :param dst: the one that receives the msg
       :type rpcc: string
       :param rpcc: the code of the endpoint associated with the channel
       :type msg: int
       :param msg: number of msgs sent by this channel
       :type bytes: int
       :param bytes: bytes sent by this channel
    """

    def __init__(self, src, dst, rpcc):
        """
        creates the associated parameters of a channel object

        :param src: the one that sends the msg
        :param dst: the one that receives the msg
        """

        self.__src = src  # source node
        self.__dst = dst  # destination node
        self.__rpcc = rpcc  # rpcc code

        self.__msg = 0  # no of msg sent
        self.__bytes = 0  # no of bytes sent

    def msg_sent(self):
        """
        Aggregates msg sent and their bytes
        :return:msgs
        """
        return self.msg

    def msg_received(self):
        """
        Aggregates msg received and their bytes. For broadcast channels, this
        is not the same as bytes sent.
        :return: bytes
        """
        return self.bytes

    def transmit(self, msg_size):
        """
        Register the transmission of a message on this channel

        :param msg_size:the number of bytes in the transmitted msg
        :return: None
        """
        self.msg += 1
        self.bytes += msg_size


class MulticastChannel(Channel):
    """
    A channel can be a multicast channel.

    This is always associated with some one-way endpoint, sending data from a single source host A to
    a destination host group B.Again, there are two channels associated with
    A and B.One channel counts the traffic sent by A, and the second channel
    counts the traffic received by all hosts in host group B. For example if
    there are 3 hosts in group B, and a message of 100 bytes is sent, one
    channel will register one additional message and 100 additional bytes,
    and the other will register 3 additional messages and 300 additional
    bytes.

    :type rx_msg: int
    :param rx_msg: total msgs received by all hosts in host_group
    :type rx_bytes: int
    :param rx_bytes:total bytes received by all hosts in host_group
    """

    def __init__(self, src, dst, rpcc):
        super().__init__(src, dst, rpcc)

        self.rx_msg = 0
        self.rx_bytes = 0

    def msg_received(self):
        return self.rx_msg

    def bytes_received(self):
        return self.rx_bytes

    def transmit(self, msg_size):
        # TODO: find correct group size
        group_size = dst.group_size
        self.rx_msg += group_size
        self.rx_bytes += group_size * msg_size


# -----------------------------------------------------------------------------
#
#   Hosts
#
# -----------------------------------------------------------------------------
class Host:
    """
    Hosts are used as nodes in the network.

    A host can represent a single network destination(site),or a set of network
    destinations.Any subclass of host is a single site.For broadcast sites one,
    has to use "HostGroup" class.

    :type nid: int (key) :param nid: the unique id of a host
    :type peers: set :param peers: includes nids of all possible destinations
    :type recv_channels: dict :param recv_channels: a list of all recv channels
    :type send_channels: dict :param send_channels: a list of all recv channels
    :type handlers: dict :param handlers: a list of all handler methods
    """

    def __init__(self, net, nid, is_bcast):
        """
        creates a host object given an id

        :param nid: unique id of a host
        """
        self.net = net  # The network the host belongs to
        self.nid = nid  # The unique id of the host
        self.is_bcast = is_bcast  # True if this is a host group
        self.incoming_channels = {}  # The channels associated with the host

        if not self.is_bcast:
            self.net.hosts[self.nid] = self
        else:
            self.net.groups[self.nid] = self

    def delete(self):
        if not self.is_bcast:
            del self.net.hosts[self.nid]
        else:
            del self.net.groups[self.nid]


class HostGroup(Host):
    """
    A host group represents a broadcast address.

    This is simply an abstract base class.The implementation of this class can
    be anything.All that this class interface provides is the methods that are
    required by the communication traffic computation.
    """

    def __init__(self, net, nid, is_bcast=True):
        super.__init__(nid, is_bcast)
        self.add_member(self)

        self.members = {}  # the members of the group

    def add_member(self, node):
        """
        Adds a host in the host group.

        :param node: the node to be added
        :return: None
        """
        self.members[node.nid] = node

    def remove_member(self, node):
        """
        Removes a host from the host group
        :param node: the node to be removed
        :return: None
        """
        del self.members[node.nid]

    def group_size(self):
        """
        Calculates the size of the host group.

        :return:group size
        """
        return len(self.members)


# -----------------------------------------------------------------------------
#
#   RPC PROTOCOL
#
# -----------------------------------------------------------------------------
class RemoteMethod:
    """Represents a method that host can call on other hosts.

    This type basically only holds the name of the remote method and whether is
    one-way or not."""
    pass


class Interface:
    """
    It is like a remote type.It represents a collection of remote methods
    that are implemented on a remote host
    """
    pass


class Protocol:
    """
    A collection of rpc interfaces.

    A protocol is the collection of RPC interfaces used in a network.
    """
    pass


class Endpoint:
    """
    The implementation of a remote method on a remote host

    An rpc call belongs to some specific rpc proxy.
    """
    pass


class Proxy:
    """
    Represents a proxy object for some host

    When a host A wants to call a remote method on host B, it makes the call
    through a proxy method, so that the network traffic can be accounted for.
    Host A is the owner of the proxy and host B is the proxied host.

    Each proxy is associated with an rpc interface, which represents the
    collection of endpoints being proxied.
    """

    def __init__(self, interface, owner):
        self.interface = interface
        self.endpoints = {}
        self.owner = owner
        self.remote_proc = {}  # the node being proxied

    def add_endpoint(self, msgtype, func):
        self.endpoint[msgtype] = func

    def connect(self, dst):
        self.remote_proc[dst.nid] = dst
