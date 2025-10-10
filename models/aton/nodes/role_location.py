from typing import Any

from neomodel import RelationshipFrom, RelationshipTo

from models.aton.nodes.base_node import BaseNode
from models.aton.relationships.exclude_from_directory import ExcludeFromDirectory
from models.aton.relationships.has_panel import HasPanel
from models.aton.relationships.role_location_serves import RoleLocationServes


class RoleLocation(BaseNode):
    # Relationships
    role_instance = RelationshipFrom("models.aton.nodes.role_instance.RoleInstance", "PERFORMED_AT")
    location = RelationshipTo("models.aton.nodes.location.Location", "LOCATION_IS")
    contacts = RelationshipTo("models.aton.nodes.contact.Contact", "HAS_LOCATION_CONTACT")

    role_network = RelationshipTo("models.aton.nodes.role_network.RoleNetwork",
                                  "ROLE_LOCATION_SERVES",
                                  model=RoleLocationServes)
    rn_behavior_health = RelationshipTo("models.aton.nodes.role_network.RoleNetwork",
                                          "IS_BEHAVIOR_HEALTH")
    rn_pcp = RelationshipTo("models.aton.nodes.role_network.RoleNetwork",
                              "IS_PCP")
    rn_specialist = RelationshipTo("models.aton.nodes.role_network.RoleNetwork","IS_SPECIALIST")
    rn_exclude_from_directory = RelationshipTo("models.aton.nodes.role_network.RoleNetwork",
                                                 "EXCLUDE_FROM_DIRECTORY",
                                                 model=ExcludeFromDirectory)
    rn_has_panel = RelationshipTo("models.aton.nodes.role_network.RoleNetwork",
                                    "HAS_PANEL",
                                    model=HasPanel)
    specialties = RelationshipTo("models.aton.nodes.role_specialty.RoleSpecialty", "PRACTICED_AT")

    primary_location = RelationshipFrom("models.aton.nodes.role_instance.RoleInstance", "PRIMARY_LOCATION_IS")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context: Any = None