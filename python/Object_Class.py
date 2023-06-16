class BIGIP_OBJECT:
    def __init__(self, name, partition):
        self.name = name
        self.partition = partition


class Node(BIGIP_OBJECT):
    def __init__(self, name, partition, address, monitor=None):
        self.address = address
        self.monitor = monitor


class Monitor(BIGIP_OBJECT):
    def __init__(self, name, partition, monitor, send=None, interval=None):
        self.monitor = monitor
        self.send = send
        self.interval = interval


class Pool(BIGIP_OBJECT):
    def __init__(
        self,
        name,
        partition,
        monitor,
        members,
        member_name,
    ):
        self.members = members
        self.member_name


class Virtual_server(BIGIP_OBJECT):
    def __init__(self, name, partition, protocol, pool, profiles, addr_translate):
        self.protocol = protocol
        self.pool = pool
        self.profiles = profiles
        self.addr_translate = addr_translate


x = Node("pool-default", "Common", "HTTPS")
print(x.monitor)
