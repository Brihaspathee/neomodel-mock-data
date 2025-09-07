from neomodel import StructuredNode, StringProperty, BooleanProperty, FloatProperty, RelationshipTo, RelationshipFrom

from models.aton.nodes.identifier import Identifier, NPI, TIN, PPGID, MedicareId, MedicaidId
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.role_instance import RoleInstance


class Organization(StructuredNode):

    name: str = StringProperty(unique_index=True, required=True)
    description: str = StringProperty(required=False)
    type: str = StringProperty(required=True)
    capitated: bool = BooleanProperty(required=False)
    pcp_practitioner_required: bool = BooleanProperty(required=False)
    atypical: bool = BooleanProperty(required=False)
    popularity: float = FloatProperty(required=False)

    npi = RelationshipTo("models.aton.nodes.identifier.NPI", "HAS_NPI")
    tin = RelationshipTo("models.aton.nodes.identifier.TIN", "HAS_TIN")
    medicare_id = RelationshipTo("models.aton.nodes.identifier.MedicareId", "HAS_MEDICAID")
    medicaid_id = RelationshipTo("models.aton.nodes.identifier.MedicaidId", "HAS_MEDICAID")
    ppg_id = RelationshipTo("models.aton.nodes.identifier.PPGID", "HAS_PPG")
    qualifications = RelationshipTo("models.aton.nodes.qualification.Qualification", "HAS_QUALIFICATION")

    role = RelationshipTo("models.aton.nodes.role_instance.RoleInstance", "HAS_ROLE")
    contracted_by = RelationshipFrom("models.aton.nodes.role_instance.RoleInstance", "CONTRACTED_BY")



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Temporary storage for identifiers
        self._pending_identifiers = {
            "npi": [],
            "tin": [],
            "medicare_id": [],
            "medicaid_id": [],
            "ppg_id": []
        }
        # Temporary storage for qualifications
        self._pending_qualifications: list[Qualification] = []
        # Temporary storage for role instances
        self._pending_role_instances: dict[str, list[RoleInstance]] = {
            "has_role": [],
            "contracted_by": []
        }

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
        elif isinstance(identifier, MedicareId):
            self._pending_identifiers["medicare_id"].append(identifier)
        elif isinstance(identifier, MedicaidId):
            self._pending_identifiers["medicaid_id"].append(identifier)
        else:
            ValueError(f"{identifier} is not a valid identifier")

    def add_role_instance(self, role_instance: RoleInstance):
        if role_instance.get_role_type() == "has_role":
            self._pending_role_instances["has_role"].append(role_instance)
        elif role_instance.get_role_type() == "contracted_by":
            self._pending_role_instances["contracted_by"].append(role_instance)
        else:
            ValueError(f"{role_instance} is not a valid role instance")

    def add_qualification(self, qualification):
        self._pending_qualifications.append(qualification)

    def get_pending_qualifications(self):
        return self._pending_qualifications

    def get_pending_identifiers(self):
        return self._pending_identifiers

    def get_pending_role_instances(self):
        return self._pending_role_instances

