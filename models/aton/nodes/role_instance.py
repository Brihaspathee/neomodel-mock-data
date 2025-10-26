from typing import Any

from neomodel import RelationshipFrom, RelationshipTo, StructuredNode

from models.aton.nodes.base_node import BaseNode
from models.aton.nodes.role_location import RoleLocation
from models.aton.nodes.role_network import RoleNetwork
from models.aton.nodes.role_specialty import RoleSpecialty


class RoleInstance(BaseNode):

    organization = RelationshipFrom("models.aton.nodes.organization.Organization", "HAS_ROLE")
    contracted_organization = RelationshipTo("models.aton.nodes.organization.Organization", "CONTRACTED_BY")
    practitioner = RelationshipFrom("models.aton.nodes.practitioner.Practitioner", "HAS_ROLE")
    role_locations = RelationshipTo("models.aton.nodes.role_location.RoleLocation", "PERFORMED_AT")
    primary_location = RelationshipTo("models.aton.nodes.role_location.RoleLocation", "PRIMARY_LOCATION_IS")
    role_networks = RelationshipTo("models.aton.nodes.role_network.RoleNetwork", "SERVES")
    specialties = RelationshipTo("models.aton.nodes.role_specialty.RoleSpecialty", "SPECIALIZES")
    prac_primary_specialty =  RelationshipTo("models.aton.nodes.role_specialty.RoleSpecialty", "PRIMARY_SPECIALTY_IS")
    disorder = RelationshipTo("models.aton.nodes.disorder.Disorder", "TREATS_DISORDER")
    healthcare_service = RelationshipTo("models.aton.nodes.healthcare_service.HealthcareService", "OFFERS_SERVICE")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context: Any = None