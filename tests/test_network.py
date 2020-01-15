from components import *
from msg_types import MsgType


def test_host():
    echo_id: int = 1
    h = Host(echo_id)

    assert h.nid == echo_id


# ----------------------------------------------------------------------------
def test_channel():
    echo_src = Host(1)
    echo_dst = Host(2)

    c = Channel(echo_src, echo_dst)

    assert c.src.nid == 1 and c.dst.nid == 2


# ----------------------------------------------------------------------------
def test_connect_1_node():
    echo_net = StarNetwork(1, Host, Host)

    assert len(echo_net.nodes) == 1 and echo_net.coord is not None

    echo_node = echo_net.nodes[0]
    echo_coord = echo_net.coord

    assert echo_node.send_channels[echo_coord] == \
        echo_coord.recv_channels[
            echo_node], " Uplink is not created correctly"


# ----------------------------------------------------------------------------
def echo_coord_handle_func(channel, msgtype, msg):
    assert msg == "Hello coord"
    msg_list = {channel.src: (msgtype, msg)}

    coord_msg = "Thanks node" + str(channel.src.nid)
    new_dst = channel.src
    new_src = channel.dst

    new_src.send(new_dst, msgtype, coord_msg)


def echo_node_handle_func(channel, msgtype, msg):
    assert msg == "Thanks node" + str(channel.dst.nid)


def test_send_msg_1_node():
    echo_net = StarNetwork(1, Host, Host)
    echo_node = echo_net.nodes[0]
    echo_coord = echo_net.coord

    echo_msg = "Hello coord"
    echo_type = MsgType("type")

    echo_coord.add_handler(echo_type, echo_coord_handle_func)
    echo_node.add_handler(echo_type, echo_node_handle_func)

    echo_node.send(echo_coord, echo_type, echo_msg)


# ----------------------------------------------------------------------------
def test_send_many_msgs():
    echo_net = StarNetwork(1, Host, Host)
    echo_node = echo_net.nodes[0]
    echo_coord = echo_net.coord

    echo_type = MsgType("type")

    echo_coord.add_handler(echo_type, echo_coord_handle_func)
    echo_node.add_handler(echo_type, echo_node_handle_func)

    for i in range(10):
        echo_msg = "Hello coord"
        echo_node.send(echo_coord, echo_type, echo_msg)
        assert echo_node.send_channels[echo_coord].msg == i+1


# ----------------------------------------------------------------------------
def test_broadcast_2_nodes():
    echo_net = StarNetwork(2, Host, Host)

    echo_msg = "Hello coord"
    echo_type = MsgType("type")

    echo_net.coord.add_handler(echo_type, echo_coord_handle_func)

    for i in range(2):
        assert echo_net.nodes[i].nid == i

        echo_net.nodes[i].add_handler(echo_type, echo_node_handle_func)
        echo_net.nodes[i].send(echo_net.coord, echo_type, echo_msg)

