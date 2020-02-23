from components import *
from tools import *
from statistics import *


@remote_class("coord")
class Coordinator(Sender):
    def __init__(self, net, nid, ifc):
        super().__init__(net, nid, ifc)

    def alert(self, arg):
        print(f"This is the {arg!r} method")

    def init(self):
        pass


@remote_class("site")
class Site(Sender):
    def __init__(self, net, nid, ifc):
        super().__init__(net, nid, ifc)

    def ack(self):
        print("Broadcast working")


###############################################################################

if __name__ == "__main__":
    n = StarNetwork(4, site_type=Site, coord_type=Coordinator)

    ifc_coord = {"alert": True, "init": True}
    n.add_interface("coord", ifc_coord)

    ifc_site = {"ack": True}
    n.add_interface("site", ifc_site)

    n.add_coord("site")
    n.add_sites(n.k, "coord")
    n.setup_connections()

    n.sites[0].send("alert", "trial")
    n.coord.send("ack", None)

    print(total_bytes(n))
    print(src_msgs(n, 0))
    dbg = None
