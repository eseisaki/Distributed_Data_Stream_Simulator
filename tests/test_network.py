from components import *


def sample():
    print("This is just a sample function")


def sample2():
    print("This is a second sample function")


def test_create_protocol():
    protocol = Protocol()
    protocol.add_method(ifc_name="A", function=sample, one_way=True)
    protocol.add_method(ifc_name="A", function=sample2, one_way=True)
    assert len(protocol.interfaces["A"].methods) == 2


def test_create_nodes():
    net = StarNetwork(3)
    assert len(net.hosts) == 1
    assert len(net.groups) == 1
    assert len(net.groups[3].members) == 3
