from neomodel import StructuredNode, StringProperty, BooleanProperty, FloatProperty, RelationshipTo, RelationshipFrom

from models.aton.nodes.contact import Contact
from models.aton.nodes.identifier import Identifier, NPI, TIN, PPGID, MedicareID, MedicaidID
from models.aton.nodes.mock_data_test import MockDataTest
from models.aton.nodes.pp_prov import PP_PROV
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.role_instance import RoleInstance


class Organization(MockDataTest):

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

    pp_prov = RelationshipFrom("models.aton.nodes.pp_prov.PP_PROV", "SOURCES")



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_ppg_id = None
        # Temporary storage for identifiers
        self._pending_identifiers = {
            "npi": [],
            "tin": [],
            "medicare_id": [],
            "medicaid_id": [],
            "ppg_id": []
        }

        self._pending_contacts: list[Contact] = []

        self._pending_qualifications: list[Qualification] = []

        self._pending_role_instances: dict[str, list[RoleInstance]] = {
            "has_role": [],
            "contracted_by": []
        }

        self._pending_portico_source: PP_PROV | None = None

    # --------------------------------
    # Associate Identifiers in Memory
    # --------------------------------
    def add_identifier(self, identifier:Identifier):
        if isinstance(identifier, NPI):
            self._pending_identifiers["npi"].append(identifier)
        elif isinstance(identifier, TIN):
            self._pending_identifiers["tin"].append(identifier)
        elif isinstance(identifier, PPGID):
            self._pending_identifiers["ppg_id"].append(identifier)
        elif isinstance(identifier, MedicareID):
            self._pending_identifiers["medicare_id"].append(identifier)
        elif isinstance(identifier, MedicaidID):
            self._pending_identifiers["medicaid_id"].append(identifier)
        else:
            ValueError(f"{identifier} is not a valid identifier")

    def add_contact(self, contact:Contact):
        self._pending_contacts.append(contact)

    def add_qualification(self, qualification:Qualification):
        self._pending_qualifications.append(qualification)

    def add_role_instance(self, role_instance: RoleInstance):
        if role_instance.get_role_type() == "has_role":
            self._pending_role_instances["has_role"].append(role_instance)
        elif role_instance.get_role_type() == "contracted_by":
            self._pending_role_instances["contracted_by"].append(role_instance)
        else:
            ValueError(f"{role_instance} is not a valid role instance")

    def get_pending_identifiers(self):
        return self._pending_identifiers

    def get_pending_contacts(self):
        return self._pending_contacts

    def get_pending_qualifications(self):
        return self._pending_qualifications

    def get_pending_role_instances(self):
        return self._pending_role_instances

    def set_portico_source(self, portico_source: PP_PROV):
        self._pending_portico_source = portico_source

    def get_portico_source(self):
        return self._pending_portico_source

