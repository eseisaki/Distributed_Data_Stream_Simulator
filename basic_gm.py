from components import *
import random as rd


class BasicCoordinator(Host):
    def __init__(self, nid):
        super().__init__(nid)
        self.global_state = {}

        def alert_handler(channel, msgtype, msg):
            new_dst = channel.src
            new_src = channel.dst

            for key, value in msg.items():
                if key not in new_src.global_state:
                    new_src.global_state[key] = value
                else:
                    new_src.global_state[key] /= 2

            new_src.send(new_dst, "new_global", new_src.global_state)

        self.add_handler("alert", alert_handler)


class BasicNode(Host):
    def __init__(self, nid):
        super().__init__(nid)
        self.local_state = {}
        self.last_sent = {}
        self.estimate = {}
        self.drift = {}

        def new_global_handler(channel, msgtype, msg):
            new_dst = channel.src
            new_src = channel.dst

            self.estimate = msg
            # initialize drift to zero
            new_src.drift = {key: 0 for key, value in new_src.drift.items()}

            print(msg)

        self.add_handler("new_global", new_global_handler)

    def update_drift(self):
        """
        Worker node updates drift as last_sent - estimate

        :return: None
        """
        for key, value in self.local_state.items():

            if key not in self.drift:
                self.drift[key] = 0
            if key not in self.last_sent:
                self.last_sent[key] = 0
            self.drift[key] = value - self.last_sent[key]

    def update_state(self, new_stream):
        """
        Worker node updates state when receives a new stream

        :param new_stream: the stream it received
        :return: None
        """
        for key, value in new_stream.items():
            if key not in self.local_state:
                self.local_state[key] = 0
            self.local_state[key] += value

    def send_alert(self, peer):
        """
        Worker node sends its local state to coord

        :param peer: where to send msg
        :return: None
        """

        for key, value in self.local_state.items():
            self.last_sent[key] = value
        # TODO: send drift instead of local_state
        self.send(peer, "alert", self.local_state)


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


if __name__ == "__main__":
    net = StarNetwork(k=2, node_type=BasicNode, coord_type=BasicCoordinator)

    # a basic simulation scenario
    for node in net.nodes:
        for time in range(2):
            for i in range(3):
                stream = stream_generator(1, 1)  # generate stream
                net.nodes[0].update_state(stream)  # update local state
                net.nodes[0].update_drift()  # update local drift
            # nodes send their local drifts every 10 streams
            net.nodes[0].send_alert(net.coord)
            dbg = 0  # only for debugging
