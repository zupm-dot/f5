class BigIP_Object:
    def __init__(self, name, partition):
        self.name = name
        self.partition = partition


class Node(BigIP_Object):
    def __init__(self, name, partition, address, monitor=None):
        self.name = name
        self.partition = partition
        self.address = address
        self.monitor = monitor


class Monitor(BigIP_Object):
    def __init__(self, name, partition, monitor, send_string=None, interval=None):
        self.name = name
        self.partition = partition
        self.monitor = monitor
        self.send_string = send_string
        self.interval = interval


class Pool(BigIP_Object):
    def __init__(self, name, partition, monitor, members, member_name):
        self.name = name
        self.partition = partition
        self.monitor = monitor
        self.members = members
        self.member_name = member_name


class Virtual_Server(BigIP_Object):
    def __init__(self, name, partition, protocol, pool, profiles, addr_translate):
        self.name = name
        self.partition = partition
        self.protocol = protocol
        self.pool = pool
        self.profiles = profiles
        self.addr_translate = addr_translate
