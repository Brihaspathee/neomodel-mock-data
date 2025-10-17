from neomodel import DoesNotExist

from models.aton.nodes.data_dictionary.dd_specialty_type import DD_SpecialtyType
from models.aton.nodes.identifier import LegacySystemIdentifier
from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.role_specialty import RoleSpecialty
import logging

log = logging.getLogger(__name__)


def create_role_specialty(role_specialty: RoleSpecialty, role_instance: RoleInstance):
    """
    Create and assign a role specialty to a role instance.

    This function establishes a connection between a provided role specialty and a role instance while
    ensuring that the specialty exists within the predefined data source. If the specialty does not
    exist, an error is logged.

    :param role_specialty: The specialty for the role, containing associated metadata and taxonomy code.
    :type role_specialty: RoleSpecialty
    :param role_instance: The role instance to which the specialty will be linked.
    :type role_instance: RoleInstance
    :return: None
    """
    try:
        # dd_specialty: DD_Specialty = DD_Specialty.nodes.filter(value=role_specialty.specialty).first()
        dd_specialty: DD_SpecialtyType = get_dd_specialty(role_specialty.specialty)
        role_specialty.specialty = dd_specialty.value
        role_specialty.taxonomyCode = dd_specialty.code
    except DoesNotExist:
        log.error(f"Speciality {role_specialty.specialty} does not exist in Aton")
    role_specialty.save()
    role_instance.specialties.connect(role_specialty)

def get_dd_specialty(specialty: str) -> DD_SpecialtyType:
    try:
        legacy_system_identifier: LegacySystemIdentifier = (
            LegacySystemIdentifier.nodes.filter(description=specialty,
                                                system="PORTICO",
                                                systemIdType="SPEC_ID").first())
        return legacy_system_identifier.dd_specialty.single()
    except DoesNotExist:
        log.error(f"No Legacy system id node exists with descript {specialty}. Hence unable to find the specialty")
    return DD_SpecialtyType.nodes.filter(value=specialty).first()