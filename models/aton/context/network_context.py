import weakref

from models.aton.nodes.identifier import LegacySystemID
from models.aton.nodes.network import Network


class NetworkContext:
    def __init__(self, network:Network):
        self.network = weakref.proxy(network)
        self._portico_source: LegacySystemID | None = None

    def set_portico_source(self, source: LegacySystemID):
        self._portico_source = source

    def get_portico_source(self):
        return self._portico_source