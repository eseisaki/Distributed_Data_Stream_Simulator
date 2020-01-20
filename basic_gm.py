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
                    new_src.global_state[key] = msg[key]
                elif new_src.global_state[key] > (msg[key] + 20):
                    new_src.global_state -= 20

            new_src.send(new_dst, "new_global", new_src.global_state)

        self.add_handler("alert", alert_handler)


class BasicNode(Host):
    def __init__(self, nid):
        super().__init__(nid)
        self.local_state = {}
        self.last_sent = {}
        self.global_state = {}
        self.drift = {}

        def new_global_handler(channel, msgtype, msg):
            new_dst = channel.src
            new_src = channel.dst

            for key, value in msg.items():
                if key not in new_src.drift:
                    new_src.drift[key] = 0
                new_src.drift[key] = new_src.last_sent[key] - value

            print(self.drift)

        self.add_handler("new_global", new_global_handler)

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
        self.last_sent = self.local_state
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
    net = StarNetwork(k=1, node_type=BasicNode, coord_type=BasicCoordinator)

    for time in range(10):
        for i in range(10):
            stream = stream_generator(5, 1)
            net.nodes[0].update_state(stream)

        net.nodes[0].send_alert(net.coord)

    dbg = 0  # only for debugging