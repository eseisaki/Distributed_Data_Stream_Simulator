from pytest import fixture
from components import *


@fixture
def echo_coord_handle_func():
    return "Thanks node"


def test_host():
    echo_id: int = 1
    h = Host(echo_id)

    assert h.nid == echo_id


def test_channel():
    echo_src = Host(1)
    echo_dst = Host(2)

    c = Channel(echo_src, echo_dst)

    assert c.src.nid == 1 and c.dst.nid == 2


def test_connect_2_nodes():
    echo_net = StarNetwork(1)

    assert len(echo_net.nodes) == 1 and echo_net.coord is not None

    echo_node = echo_net.nodes[0]
    echo_coord = echo_net.coord

    assert echo_node.send_channels[echo_coord] ==\
        echo_coord.recv_channels[echo_node], " Uplink is not created correctly"


# TODO: understand and create echo_handler_functions
def test_send_msg_1_node(echo_coord_handle_func):

    echo_net = StarNetwork(1)
    echo_node = echo_net.nodes[0]
    echo_coord = echo_net.coord

    msg_node = "Hello coord"

    echo_coord.add_handler("string", echo_coord_handle_func)
    echo_node.send(echo_coord, "string", msg_node)

def test_network_with_2_nodes():
    pass
