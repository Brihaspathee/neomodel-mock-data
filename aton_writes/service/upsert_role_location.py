from aton_writes.service.upsert_role_specialty import create_role_specialty
from models.aton.nodes.data_dictionary.dd_specialty import DD_Specialty
from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.location import Location
from neomodel.exceptions import DoesNotExist
from repository.location_repo import get_or_create_location
from repository. contact_repo import create_contacts
import logging

log = logging.getLogger(__name__)


def process_role_locations(role_instance:RoleInstance):
    """
    Processes and associates pending role locations for the given `RoleInstance`.

    This function iterates over all pending role locations of the provided `RoleInstance`.
    It performs operations such as retrieving or creating `Location` instances,
    saving role locations, associating primary locations, creating contacts, and connecting
    specialties to their respective locations. Additionally, connections between role
    locations, locations, and the `RoleInstance` are established. The function also logs
    details of each processed role location.

    :param role_instance: A `RoleInstance` object containing pending role locations
                          to be processed and connected.
    :type role_instance: RoleInstance
    :return: None
    """
    for role_location in role_instance.get_pending_rls():
        location: Location = role_location.get_location()
        location = get_or_create_location(location)
        role_location.save()
        if role_location.get_is_primary():
            role_instance.primary_location.connect(role_location)
        create_contacts(role_location)
        for speciality in role_location.get_pending_specialties():
            create_role_specialty(speciality, role_instance)
            speciality.role_locations.connect(role_location)
        role_location.location.connect(location)
        role_instance.role_locations.connect(role_location)
        log.debug(f"Role location saved to Aton its element id is: {role_location.element_id}")


