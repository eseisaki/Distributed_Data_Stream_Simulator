from components import *


class EchoSim:
    """
        Helpful class to avoid boilerplate code in tests.

        When initialized it creates a star network with k sites.
    """

    def __init__(self, k):
        @remote_class("coord")
        class Coordinator(Sender):
            def __init__(self, net, nid, ifc):
                super().__init__(net, nid, ifc)

            def method(self, arg):
                assert arg == "a msg"

        @remote_class("site")
        class Site(Sender):
            def __init__(self, net, nid, ifc):
                super().__init__(net, nid, ifc)

            def method2(self, arg):
                assert arg == "a coord msg"

        self.n = StarNetwork(k, coord_type=Coordinator, site_type=Site)

        interface1 = {"method": True}
        interface2 = {"method2": True}

        self.n.add_interface("coord", interface1)
        self.n.add_interface("site", interface2)

        self.n.add_sites(k, "coord")
        self.n.add_coord("site")

        self.n.setup_connections()


###############################################################################
def test_create_protocol():
    n = Network()
    interface = {"method1": True, "method2": False}

    n.add_interface("trial", interface)

    assert bool(n.protocol.interfaces["trial"])


###############################################################################
def test_create_nodes(k=4):
    n = StarNetwork(k)
    interface = {"method": True}

    n.add_interface("trial", interface)
    n.add_sites(k, "trial")

    assert len(n.sites) == k


###############################################################################
def test_create_network(k=4):
    sim = EchoSim(k)
    assert len(sim.n.channels) == k + 1


###############################################################################
def test_send_oneway(k=4):
    sim = EchoSim(k)

    for site in sim.n.sites.values():
        site.send("method", "a msg")


###############################################################################
def test_broadcast(k=4):
    sim = EchoSim(k)

    sim.n.coord.send("method2", "a coord msg")


###############################################################################
def test_iterations():
    assert 0 == 1


###############################################################################
def test_total_msgs():
    assert 0 == 1


###############################################################################
def test_total_bytes():
    assert 0 == 1


###############################################################################
def test_broadcast_msgs():
    assert 0 == 1


###############################################################################
def test_broadcast_bytes():
    assert 0 == 1


###############################################################################
def test_endpoint_msgs():
    assert 0 == 1


###############################################################################
def test_endpoint_bytes():
    assert 0 == 1
