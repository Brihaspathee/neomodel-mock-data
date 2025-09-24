from neomodel import RelationshipFrom, RelationshipTo, StructuredNode

from models.aton.nodes.mock_data_test import MockDataTest
from models.aton.nodes.role_location import RoleLocation
from models.aton.nodes.role_network import RoleNetwork


class RoleInstance(MockDataTest):

    _role_type: str = None
    organization = RelationshipFrom("models.aton.nodes.organization.Organization", "HAS_ROLE")
    contracted_organization = RelationshipTo("models.aton.nodes.organization.Organization", "CONTRACTED_BY")
    practitioner = RelationshipFrom("models.aton.nodes.practitioner.Practitioner", "HAS_ROLE")
    role_locations = RelationshipTo("models.aton.nodes.role_location.RoleLocation", "PERFORMED_AT")
    primary_location = RelationshipTo("models.aton.nodes.role_location.RoleLocation", "PRIMARY_LOCATION_IS")
    role_networks = RelationshipTo("models.aton.nodes.role_network.RoleNetwork", "SERVES")
    specialties = RelationshipTo("models.aton.nodes.role_specialty.RoleSpecialty", "SPECIALIZES")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pending_rls: list[RoleLocation] = []
        self._pending_rns: list[RoleNetwork] = []

    def add_pending_rl(self, rl: RoleLocation):
        self._pending_rls.append(rl)

    def get_pending_rls(self) -> list[RoleLocation]:
        return self._pending_rls

    def set_role_type(self, role_type: str):
        self._role_type = role_type

    def get_role_type(self):
        return self._role_type

    def add_pending_rn(self, rn: RoleNetwork):
        self._pending_rns.append(rn)

    def get_pending_rns(self) -> list[RoleNetwork]:
        return self._pending_rns

    # def __str__(self):
    #     return f"Role Instance Type: {self._role_type}"