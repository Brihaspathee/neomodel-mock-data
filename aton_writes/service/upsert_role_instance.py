from models.aton.nodes.organization import Organization
from aton_writes.service.upsert_role_location import process_role_locations
from aton_writes.service.upsert_role_network import process_role_networks
import logging

from models.aton.nodes.role_instance import RoleInstance

log = logging.getLogger(__name__)


def process_role_instance(org: Organization,):
    """
    Processes pending role instances for an organization. This function iterates through all pending role instances
    grouped by their type within the organization, performs necessary actions such as saving them, processing their
    locations and networks, and connecting them to the organization's role relationships.

    :param org: The organization instance whose pending role instances need to be processed.
    :type org: Organization
    :return: None
    """
    for role_type, role_instance_list in org.get_pending_role_instances().items():
        if role_type == "has_role":
            for role_instance in role_instance_list:
                role_instance.save()
                log.debug(f"Role instance saved to Aton its element id is: {role_instance.element_id}")
                process_role_locations(role_instance)
                process_role_networks(role_instance)
                org.role.connect(role_instance)


