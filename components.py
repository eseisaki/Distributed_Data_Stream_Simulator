import functools


###############################################################################
#
# Decorators
#
###############################################################################
def remote_class(ifc):
    def decorator_remote(cls):
        @functools.wraps(cls)
        def wrapper_decorator(*args, **kwargs):
            instance = cls(*args, **kwargs)
            if ifc in instance.net.protocol.interfaces:
                interface = instance.net.protocol.interfaces[ifc]
                for name in interface.methods.keys():
                    obj = getattr(instance, str(name), None)
                    if not callable(obj):
                        raise TypeError(f"The {str(name)!r} function must be "
                                        f"implemented")
            return instance

        return wrapper_decorator

    return decorator_remote


###############################################################################
#
# Channels
#
###############################################################################
class Channel:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

        self.msg = 0
        self.bytes = 0

    def transmit(self, msg_size):
        self.msg += 1
        self.bytes += msg_size


###############################################################################
#
# Hosts
#
###############################################################################

class Host:
    def __init__(self, net):
        self.net = net
        self.incoming_channels = {}


###############################################################################
#
# Protocol
#
###############################################################################

class Interface:
    def __init__(self, name):
        self.name = name
        self.methods = {}

    def add_method(self, name, one_way):
        if name not in self.methods:
            self.methods[name] = one_way


class Protocol:
    def __init__(self):
        self.interfaces = {}

    def add_interface(self, ifc, methods):
        for key, value in methods.items():
            self.add_method(ifc, key, value)

    def add_method(self, ifc, name, one_way):
        if ifc not in self.interfaces:
            self.interfaces[ifc] = Interface(ifc)
        self.interfaces[ifc].add_method(name, one_way)


class Endpoint:
    def __init__(self, func, req_channel, resp_channel=None):
        self.send = func
        self.req_channel = req_channel
        self.resp_channel = resp_channel


###############################################################################
#
# Proxy
#
###############################################################################

class Proxy:
    def __init__(self, ifc):
        self.ifc = ifc
        self.owner = None
        self.proxied = None
        self.endpoints = {}

    def create_endpoints(self):
        ifc_obj = self.owner.net.protocol.interfaces[self.ifc]

        for name, one_way in ifc_obj.methods.items():
            send = getattr(self.proxied, name)
            req_channel = Channel(self.owner, self.proxied)
            if not one_way:
                self.endpoints[name] = Endpoint(send, req_channel)
            else:
                resp_channel = Channel(self.proxied, self.owner)
                self.endpoints[name] = Endpoint(send, req_channel,
                                                resp_channel)


class Sender(Host):
    def __init__(self, net, ifc):
        super().__init__(net)
        if ifc not in self.net.protocol.interfaces:
            raise TypeError(f"There is no {ifc!r} interface")
        self.proxy = Proxy(ifc)

    def connect_proxy(self, proxied):
        if proxied not in self.net.hosts:
            TypeError(f"There is no {proxied!r} host")

        self.proxy.owner = self
        self.proxy.proxied = proxied

        self.proxy.create_endpoints()

    def send(self, method: str, msg):
        self.proxy.endpoints[method].send(msg)
        self.proxy.endpoints[method].req_channel.transmit(100)


###############################################################################
#
# Networks
#
###############################################################################
class Network:
    def __init__(self):
        self.protocol = Protocol()
        self.hosts = {}

    def add_interface(self, ifc, methods):
        self.protocol.add_interface(ifc, methods)

    def add_method(self, ifc, m_name, one_way):
        self.protocol.add_method(ifc, m_name, one_way)

    def add_host(self, nid):
        if not bool(self.protocol.interfaces):
            raise TypeError("Interfaces must be added before host "
                            "initialization")
        self.hosts[nid] = Host(self)

    @staticmethod
    def link(src, dst):
        src.connect_proxy(dst)


class StarNetwork(Network):
    def __init__(self, k, site_type, coord_type):
        super().__init__()
        self.site_type = site_type
        self.coord_type = coord_type
        self.coord = None

    def add_coord(self):
        self.hosts[None] = self.coord_type(self)
        self.coord = self.hosts[None]

    def add_site(self, nid, ifc):
        self.hosts[nid] = self.site_type(self, ifc)
