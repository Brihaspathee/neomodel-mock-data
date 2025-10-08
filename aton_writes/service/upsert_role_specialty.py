from neomodel import DoesNotExist

from models.aton.nodes.data_dictionary.dd_specialty import DD_Specialty
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
        dd_specialty: DD_Specialty = DD_Specialty.nodes.filter(value=role_specialty.specialty).first()
        role_specialty.taxonomyCode = dd_specialty.taxonomyCode
    except DoesNotExist:
        log.error(f"Speciality {role_specialty.specialty} does not exist in Aton")
    role_specialty.save()
    role_instance.specialties.connect(role_specialty)