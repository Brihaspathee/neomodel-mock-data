from typing import Any

from neomodel import StructuredNode, StringProperty, BooleanProperty, FloatProperty, RelationshipTo, RelationshipFrom

from models.aton.nodes.base_node import BaseNode
from models.aton.nodes.contact import Contact
from models.aton.nodes.identifier import Identifier, NPI, TIN, PPGID, MedicareID, MedicaidID, LegacySystemID
from models.aton.nodes.practitioner import Practitioner
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.role_instance import RoleInstance


class Organization(BaseNode):

    name: str = StringProperty(unique_index=True, required=True)
    alias: str = StringProperty(required=False)
    description: str = StringProperty(required=False)
    type: str = StringProperty(required=True)
    capitated: bool = BooleanProperty(required=False)
    pcp_practitioner_required: bool = BooleanProperty(required=False)
    atypical: bool = BooleanProperty(required=False)
    popularity: float = FloatProperty(required=False)

    #------------------------------------------------------------------------------
    # Self-Referential Relationships
    #------------------------------------------------------------------------------
    parent = RelationshipTo("Organization", "PART_OF")
    children = RelationshipFrom("Organization", "PART_OF")

    pp_prov = RelationshipFrom("models.aton.nodes.pp_prov.PP_PROV", "SOURCES")
    npi = RelationshipTo("NPI", "HAS_NPI")
    tin = RelationshipTo("TIN", "HAS_TIN")
    medicare_id = RelationshipTo("MedicareID", "HAS_MEDICARE_ID")
    medicaid_id = RelationshipTo("MedicaidID", "HAS_MEDICAID_ID")
    ppg_id = RelationshipTo("PPGID", "HAS_PPG_ID")

    contacts = RelationshipTo("models.aton.nodes.contact.Contact",
                              "HAS_ORGANIZATION_CONTACT")

    qualifications = RelationshipTo("models.aton.nodes.qualification.Qualification",
                                    "HAS_QUALIFICATION")

    role = RelationshipTo("RoleInstance", "HAS_ROLE")
    contracted_by = RelationshipFrom("RoleInstance", "CONTRACTED_BY")
    legacy_system_id = RelationshipTo("models.aton.nodes.identifier.Identifier","HAS_LEGACY_SYSTEM_ID")



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_ppg_id = None
        self.context: Any = None



