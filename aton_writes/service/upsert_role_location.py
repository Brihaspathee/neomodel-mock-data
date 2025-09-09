from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.location import Location
from repository.location_repo import get_or_create_location
from repository. contact_repo import create_contacts
import logging

log = logging.getLogger(__name__)


def process_role_locations(role_instance:RoleInstance):
    for role_location in role_instance.get_pending_rls():
        location: Location = role_location.get_location()
        location = get_or_create_location(location)
        role_location.save()
        create_contacts(role_location)
        role_location.location.connect(location)
        role_instance.role_locations.connect(role_location)
        log.info(f"Role location saved to Aton its element id is: {role_location.element_id}")


