from components import *
import random as rd


class BasicCoordinator(Host):
    def __init__(self, global_state):
        super()
        self.global_state = global_state  # initialize coordinator


class BasicNode(Host):
    def __init__(self):
        super()
        self.local_state = {}

    def update_state(self, new_stream):
        key, value = new_stream
        self.local_state[key] += value


# TODO: create basic functionality when coordinator receives a msg from a node
def start_round(channel, msg_type, msg):
    pass


def start_subround(channel, msg_type, msg):
    pass


# TODO: create basic functionality when node receives a msg from coordinator
def receive_streams(channel, msg_type, msg):
    pass


# TODO: create a stream generator
def make_stream():
    return rd.randint(1, 4), rd.randint(1, 10)


# TODO: create a simulation scenario
if __name__ == "__main__":
    # initialize network
    net = StarNetwork(2, node_type=BasicNode, coord_type=BasicCoordinator)

    # initialize handler func
    net.coord.add_handler(("string", "coord"), receive_streams)
    for node in net.nodes:
        net.node.add_handler(("int", "round"), start_round)
        net.node.add_handler(("int", "subround"), start_subround)
