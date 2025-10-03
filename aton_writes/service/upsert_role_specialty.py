from neomodel import DoesNotExist

from models.aton.nodes.data_dictionary.dd_specialty import DD_Specialty
from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.role_specialty import RoleSpecialty
import logging

log = logging.getLogger(__name__)


def create_role_specialty(role_specialty: RoleSpecialty, role_instance: RoleInstance):
    try:
        dd_specialty: DD_Specialty = DD_Specialty.nodes.filter(value=role_specialty.specialty).first()
        role_specialty.taxonomyCode = dd_specialty.taxonomyCode
    except DoesNotExist:
        log.error(f"Speciality {role_specialty.specialty} does not exist in Aton")
    role_specialty.save()
    role_instance.specialties.connect(role_specialty)