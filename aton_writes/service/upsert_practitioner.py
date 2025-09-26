from aton_writes.service.upsert_role_location import process_role_locations
from aton_writes.service.upsert_role_network import process_role_networks
from models.aton.nodes.identifier import LegacySystemID
from models.aton.nodes.organization import Organization
from models.aton.nodes.practitioner import Practitioner
from models.aton.nodes.role_instance import RoleInstance
from repository.practitioner_repo import get_practitioner_by_prac_id
from repository.role_instance_repo import get_role_instance_for_prac_org, get_role_instances
import logging

log = logging.getLogger(__name__)


def upsert_practitioner(organization: Organization):
    log.debug(f"About to upsert practitioners to organization {organization.name} with element id {organization.element_id}")
    for practitioner in organization.get_pending_practitioners():
        log.debug(f"Practitioners is: {practitioner}")
        existing_prac = get_practitioner_by_prac_id(practitioner.get_portico_source().value)
        if existing_prac:
            log.debug(f"Practitioner already exists with element id {existing_prac.element_id}")
            role_instance = practitioner.get_pending_role_instance()
            existing_ris = get_role_instances(existing_prac, organization)
            if not existing_ris:
                role_instance.save()
                existing_prac.role.connect(role_instance)
                role_instance.contracted_organization.connect(organization)
                process_role_locations(role_instance)
                process_role_networks(role_instance)
        else:
            log.debug(f"Practitioner does not exist")
            create_practitioner(practitioner, organization)


def create_practitioner(practitioner: Practitioner, organization: Organization):
    log.debug(f"About to create practitioner to organization {organization.name} with element id {organization.element_id}")
    practitioner.save()
    aton_prac: LegacySystemID = practitioner.get_portico_source()
    aton_prac.save()
    aton_prac.practitioner.connect(practitioner)
    role_instance: RoleInstance = practitioner.get_pending_role_instance()
    log.debug(f"Role instance is: {type(role_instance)}")
    role_instance.save()
    practitioner.role.connect(role_instance)
    role_instance.contracted_organization.connect(organization)
    process_role_locations(role_instance)
    process_role_networks(role_instance)
    log.debug(f"Practitioner created with element id {practitioner.element_id}")