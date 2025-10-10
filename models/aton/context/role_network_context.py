import weakref

from models.aton.nodes.network import Network
from models.aton.nodes.role_location import RoleLocation
from models.aton.nodes.role_network import RoleNetwork
from models.aton.relationships.role_location_serves import RoleLocationServes


class AssociatedRL:
    def __init__(self, role_location: RoleLocation,
                 rls_edges: list[RoleLocationServes] = None):
        self.role_location = role_location
        if rls_edges is None:
            self.rls_edges = []
        else:
            self.rls_edges = rls_edges

class RoleNetworkContext:

    def __init__(self, role_network:RoleNetwork):
        self.role_network = weakref.proxy(role_network)
        self._network: Network | None = None
        self._assoc_rls: list[AssociatedRL] = []
        self._is_pcp: bool = False
        self._is_behavior_health: bool = False
        self._is_specialist: bool = False

    def set_network(self, network: Network):
        self._network = network

    def get_network(self) -> Network:
        return self._network

    def add_assoc_rl(self, rl: AssociatedRL):
        self._assoc_rls.append(rl)

    def get_assoc_rls(self) -> list[AssociatedRL]:
        return self._assoc_rls

    def set_is_pcp(self, is_pcp: bool):
        self._is_pcp = is_pcp

    def get_is_pcp(self) -> bool:
        return self._is_pcp

    def set_is_behavior_health(self, is_behavior_health: bool):
        self._is_behavior_health = is_behavior_health

    def get_is_behavior_health(self) -> bool:
        return self._is_behavior_health

    def set_is_specialist(self, is_specialist: bool):
        self._is_specialist = is_specialist

    def get_is_specialist(self) -> bool:
        return self._is_specialist