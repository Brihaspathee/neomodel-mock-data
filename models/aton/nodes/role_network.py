from neomodel import StructuredNode, BooleanProperty, RelationshipTo, RelationshipFrom

from models.aton.nodes.base_node import BaseNode
from models.aton.nodes.network import Network
from models.aton.nodes.role_location import RoleLocation
from models.aton.relationships.exclude_from_directory import ExcludeFromDirectory
from models.aton.relationships.has_panel import HasPanel
from models.aton.relationships.role_location_serves import RoleLocationServes

class AssociatedRL:
    def __init__(self, role_location: RoleLocation,
                 rls_edges: list[RoleLocationServes] = None):
        self.role_location = role_location
        if rls_edges is None:
            self.rls_edges = []
        else:
            self.rls_edges = rls_edges

class RoleNetwork(BaseNode):
    suppress_pcp_assignment: bool = BooleanProperty(default=False)

    # Relationships
    network = RelationshipTo("models.aton.nodes.network.Network", "NETWORK_IS")
    role_instance = RelationshipFrom("models.aton.nodes.role_instance.RoleInstance", "SERVES")
    role_location = RelationshipFrom("models.aton.nodes.role_location.RoleLocation",
                                            "ROLE_LOCATION_SERVES",
                                            model=RoleLocationServes)
    rl_behavior_health = RelationshipFrom("models.aton.nodes.role_location.RoleLocation",
                                          "BEHAVIOR_HEALTH")
    rl_pcp = RelationshipFrom("models.aton.nodes.role_location.RoleLocation",
                              "PCP")
    rl_exclude_from_directory = RelationshipFrom("models.aton.nodes.role_location.RoleLocation",
                                                "EXCLUDE_FROM_DIRECTORY",
                                                 model=ExcludeFromDirectory)
    rl_has_panel = RelationshipFrom("models.aton.nodes.role_location.RoleLocation",
                                   "HAS_PANEL",
                                    model=HasPanel)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._network: Network | None = None
        self._pending_assoc_rls: list[AssociatedRL] = []


    def set_network(self, network: Network):
        self._network = network

    def get_network(self) -> Network:
        return self._network

    def add_pending_assoc_rl(self, rl: AssociatedRL):
        self._pending_assoc_rls.append(rl)

    def get_pending_assoc_rls(self) -> list[AssociatedRL]:
        return self._pending_assoc_rls
