from components import *
import random as rd


class BasicCoordinator(Host):
    def __init__(self, nid):
        super().__init__(nid)
        self.__global_state = {}  # the global_state
        self.__recv_msgs = {}  # received msgs

        self.add_handler("alert", self.__alert_handler)  # add "alert" handler

    @staticmethod
    def __alert_handler(channel, msgtype, msg):
        """
        The handler to be executed when coord receives an alert from nodes

        :param channel: from where the msg was sent
        :param msgtype: the type of the msg
        :param msg: the body of the msg
        :return: None
        """
        new_dst = channel.src
        new_src = channel.dst
        # save every new msg from each node
        new_src.__recv_msgs[new_dst] = msg

        # do sth for every msg received; maybe temp
        for key, value in msg.items():
            if key not in new_src.__global_state:
                new_src.__global_state[key] = value
            else:
                new_src.__global_state[key] /= 2

        # wait for all nodes to send their msg
        # and then broadcast msg to each node
        if all(k in new_src.__recv_msgs for k in new_src.send_channels.keys()):
            new_src.broadcast("new_global", new_src.__global_state)
            print("total msgs:", new_src.get_broad_msg())
            print("total_bytes:", new_src.get_broad_bytes())


class BasicNode(Host):
    def __init__(self, nid):
        super().__init__(nid)
        self.__local_state = {}  # the local_state
        self.__last_state = {}  # the last_state before sending an alert
        self.__estimate = {}  # the stored estimate coming from coord
        self.drift = {}  # the local drift

        self.add_handler("new_global", self.__new_global_handler)

    @staticmethod
    def __new_global_handler(channel, msgtype, msg):
        new_dst = channel.src
        new_src = channel.dst

        new_src.__estimate = msg
        # initialize drift to zero
        new_src.drift = {key: 0 for key, value in new_src.drift.items()}

        # TODO: Find a way to aggregate broadcast bytes
        print("msg:", msg, "nid:", new_src.nid)

    def update_drift(self):
        """
        Worker node updates drift as last_state - estimate

        :return: None
        """
        for key, value in self.__local_state.items():

            if key not in self.drift:
                self.drift[key] = 0
            if key not in self.__last_state:
                self.__last_state[key] = 0
            self.drift[key] = value - self.__last_state[key]

    def update_state(self, new_stream):
        """
        Worker node updates state when receives a new stream

        :param new_stream: the stream it received
        :return: None
        """
        for key, value in new_stream.items():
            if key not in self.__local_state:
                self.__local_state[key] = 0
            self.__local_state[key] += value

    def send_alert(self, peer):
        """
        Worker node sends its local state to coord

        :param peer: where to send msg
        :return: None
        """
        for key, value in self.__local_state.items():
            self.__last_state[key] = value
        self.send(peer, "alert", self.__local_state)


def stream_generator(keys, length):
    """
    Returns a stream of (key,value) pairs

    :param keys: max number of keys
    :param length: overall length of a stream
    :return: a dictionary of (k,v) pairs
    """
    res = {}
    for i in range(length):
        res[rd.randint(1, keys)] = 1
    return res


def simulation(node_a, coord):
    # a basic simulation scenario
    for i in range(10):
        stream = stream_generator(1, 1)  # generate stream
        node_a.update_state(stream)  # update local state
        node_a.update_drift()  # update local drift
    # nodes send their local drifts every 10 streams
    node_a.send_alert(coord)


if __name__ == "__main__":
    net = StarNetwork(k=10, node_type=BasicNode, coord_type=BasicCoordinator)
    for node in net.nodes:
        simulation(node, net.coord)