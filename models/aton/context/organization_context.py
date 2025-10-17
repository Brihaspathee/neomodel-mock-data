import weakref

from models.aton.nodes.contact import Contact
from models.aton.nodes.identifier import Identifier, NPI, TIN, MedicaidID, MedicareID, PPGID, LegacySystemIdentifier
from models.aton.nodes.organization import Organization
from models.aton.nodes.practitioner import Practitioner
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.role_instance import RoleInstance


class OrganizationContext:
    """
    Represents the organizational context and manages associated identifiers and contacts.

    This class is used to manage the operational context for a specific organization.
    It encapsulates the identifiers linked to the organization, such as NPI (National
    Provider Identifier), TIN (Taxpayer Identification Number), Medicare ID, Medicaid
    ID, and PPG ID (Professional Practice Group Identifier). It also includes a list
    of contacts associated with the organization.

    :ivar organization: A proxy reference to the associated `Organization` instance.
    :type organization: Organization
    :ivar _identifiers: A dictionary containing lists of various types of identifiers
        related to the organization. Keys include "npi", "tin", "medicare_id",
        "medicaid_id", and "ppg_id".
    :type _identifiers: dict[str, list[Identifier]]
    :ivar _contacts: A list of `Contact` objects associated with the organization.
    :type _contacts: list[Contact]
    """
    def __init__(self, org:Organization):
        self.organization = weakref.proxy(org)
        self._parent_ppg_id: str | None = None
        self._portico_source: LegacySystemIdentifier | None = None
        self._identifiers = {
            "npi": [],
            "tin": [],
            "medicare_id": [],
            "medicaid_id": [],
            "ppg_id": []
        }
        self._contacts: list[Contact] = []
        self._qualifications: list[Qualification] = []
        self._role_instances: dict[str, list[RoleInstance]] = {
            "has_role": [],
            "contracted_by": []
        }
        self._practitioners: list[Practitioner] = []

    def add_identifier(self, identifier:Identifier):
        """
        Adds a given identifier to the corresponding list within `_identifiers`
        based on its type. The method categorizes identifiers as NPI, TIN,
        PPGID, MedicareID, or MedicaidID, and stores them in the appropriate
        category. If the provided identifier does not match any of these
        categories, a ValueError is raised.

        :param identifier: The identifier object to be added. Accepted types
            include NPI, TIN, PPGID, MedicareID, and MedicaidID.
        :type identifier: Identifier
        :return: None
        :raises ValueError: If the identifier type does not match any supported
            category.
        """
        if isinstance(identifier, NPI):
            self._identifiers["npi"].append(identifier)
        elif isinstance(identifier, TIN):
            self._identifiers["tin"].append(identifier)
        elif isinstance(identifier, PPGID):
            self._identifiers["ppg_id"].append(identifier)
        elif isinstance(identifier, MedicareID):
            self._identifiers["medicare_id"].append(identifier)
        elif isinstance(identifier, MedicaidID):
            self._identifiers["medicaid_id"].append(identifier)
        else:
            ValueError(f"{identifier} is not a valid identifier")

    def get_identifiers(self):
        """
        Returns a dictionary containing lists of various types of identifiers
        """
        return self._identifiers

    def add_contact(self, contact:Contact):
        """
        Adds a given contact to the `_contacts` list.
        """
        self._contacts.append(contact)

    def get_contacts(self):
        """
        Returns a list of contacts associated with the organization.
        """
        return self._contacts

    def set_portico_source(self, portico_source: LegacySystemIdentifier):
        """
        Sets the portico source for the organization.
        """
        self._portico_source = portico_source

    def get_portico_source(self):
        """
        Returns the portico source for the organization.
        """
        return self._portico_source

    def add_qualification(self, qualification: Qualification):
        """
        Adds a new qualification to the internal list of qualifications.

        :param qualification: The qualification to be added to the internal list.
        :type qualification: Qualification
        """
        self._qualifications.append(qualification)

    def get_qualifications(self):
        """
        Retrieves the qualifications associated with the instance.
        """
        return self._qualifications

    def add_role_instance(self, role_instance: RoleInstance):
        """
        Adds a new role instance to the internal list of role instances.
        """
        if role_instance.context.get_role_type() == "has_role":
            self._role_instances["has_role"].append(role_instance)
        elif role_instance.context.get_role_type() == "contracted_by":
            self._role_instances["contracted_by"].append(role_instance)
        else:
            ValueError(f"{role_instance} is not a valid role instance")

    def get_role_instances(self):
        """
        Retrieves the role instances associated with the instance.
        """
        return self._role_instances

    def add_practitioner(self, practitioner: Practitioner):
        """
        Adds a new practitioner to the internal list of practitioners.
        """
        self._practitioners.append(practitioner)

    def get_practitioners(self):
        """
        Retrieves the practitioners associated with the instance.
        """
        return self._practitioners

    def set_parent_ppg_id(self, ppg_id: str):
        self._parent_ppg_id = ppg_id

    def get_parent_ppg_id(self):
        return self._parent_ppg_id
