from components import *


@remote_class("coord")
class Coordinator(Host):
    def __init__(self, net):
        super().__init__(net)

    def alert(self, arg):
        print(f"This is the {arg!r} method")

    def init(self):
        pass


class Site(Sender):
    def __init__(self, net, ifc):
        super().__init__(net, ifc)


###############################################################################

if __name__ == "__main__":
    n = StarNetwork(1, site_type=Site, coord_type=Coordinator)

    ifc_coord = {"alert": True, "init": True}
    n.add_interface("coord", ifc_coord)

    n.add_coord()
    n.add_site(3, "coord")

    n.link(n.hosts[3], n.coord)
    n.hosts[3].send("alert", "help me")
    dbg = None
