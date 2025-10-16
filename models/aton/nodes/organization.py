from typing import Any

from neomodel import StringProperty, BooleanProperty, FloatProperty, RelationshipTo, RelationshipFrom

from models.aton.nodes.base_node import BaseNode


class Organization(BaseNode):

    name: str = StringProperty(unique_index=True, required=True)
    alias: str = StringProperty(required=False)
    description: str = StringProperty(required=False)
    type: str = StringProperty(required=True)
    capitated: bool = BooleanProperty(required=False)
    pcp_practitioner_required: bool = BooleanProperty(required=False, db_property='pcpPractitionerRequired')
    atypical: bool = BooleanProperty(required=False)
    popularity: float = FloatProperty(required=False)

    #------------------------------------------------------------------------------
    # Self-Referential Relationships
    #------------------------------------------------------------------------------
    parent = RelationshipTo("Organization", "PART_OF")
    children = RelationshipFrom("Organization", "PART_OF")

    pp_prov = RelationshipFrom("models.aton.nodes.pp_prov.PP_PROV", "SOURCES")
    npi = RelationshipTo("models.aton.nodes.identifier.NPI", "HAS_NPI")
    tin = RelationshipTo("models.aton.nodes.identifier.TIN", "HAS_TIN")
    medicare_id = RelationshipTo("models.aton.nodes.identifier.MedicareID", "HAS_MEDICARE_ID")
    medicaid_id = RelationshipTo("models.aton.nodes.identifier.MedicaidID", "HAS_MEDICAID_ID")
    ppg_id = RelationshipTo("models.aton.nodes.identifier.PPGID", "HAS_PPG_ID")

    contacts = RelationshipTo("models.aton.nodes.contact.Contact",
                              "HAS_ORGANIZATION_CONTACT")

    qualifications = RelationshipTo("models.aton.nodes.qualification.Qualification",
                                    "HAS_QUALIFICATION")

    role = RelationshipTo("models.aton.nodes.role_instance.RoleInstance", "HAS_ROLE")
    contracted_by = RelationshipFrom("models.aton.nodes.role_instance.RoleInstance", "CONTRACTED_BY")
    legacy_system_id = RelationshipTo("models.aton.nodes.identifier.LegacySystemID","HAS_LEGACY_SYSTEM_ID")



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context: Any = None



