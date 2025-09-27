from models.aton.nodes.data_dictionary.dd_specialty import DD_Specialty
from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.location import Location
from neomodel.exceptions import DoesNotExist
from repository.location_repo import get_or_create_location
from repository. contact_repo import create_contacts
import logging

log = logging.getLogger(__name__)


def process_role_locations(role_instance:RoleInstance):
    for role_location in role_instance.get_pending_rls():
        location: Location = role_location.get_location()
        location = get_or_create_location(location)
        role_location.save()
        if role_location.get_is_primary():
            role_instance.primary_location.connect(role_location)
        create_contacts(role_location)
        for speciality in role_location.get_pending_specialties():
            try:
                dd_specialty: DD_Specialty = DD_Specialty.nodes.filter(name=speciality.specialty).first()
                speciality.taxonomy = dd_specialty.taxonomy
            except DoesNotExist:
                log.error(f"Speciality {speciality.specialty} does not exist in Aton")
            speciality.save()
            role_instance.specialties.connect(speciality)
            speciality.role_locations.connect(role_location)
        role_location.location.connect(location)
        role_instance.role_locations.connect(role_location)
        log.debug(f"Role location saved to Aton its element id is: {role_location.element_id}")


