from neomodel import DoesNotExist

from aton_writes.service.upsert_role_location import process_role_locations
from aton_writes.service.upsert_role_network import process_role_networks
from aton_writes.service.upsert_role_specialty import create_role_specialty
from models.aton.nodes.data_dictionary.dd_specialty import DD_Specialty
from models.aton.nodes.identifier import LegacySystemID, TIN
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
                process_prac_role_specialties(role_instance)
        else:
            log.debug(f"Practitioner does not exist")
            create_practitioner(practitioner, organization)


def create_practitioner(practitioner: Practitioner, organization: Organization):
    log.debug(f"About to create practitioner to organization {organization.name} with element id {organization.element_id}")
    practitioner.save()
    aton_prac: LegacySystemID = practitioner.get_portico_source()
    aton_prac.save()
    aton_prac.practitioner.connect(practitioner)
    create_identifiers(prac=practitioner)
    create_qualifications(prac=practitioner)
    role_instance: RoleInstance = practitioner.get_pending_role_instance()
    log.debug(f"Pending Role Specialties: {role_instance.get_pending_prac_rs()}")
    log.debug(f"Role instance is: {type(role_instance)}")
    role_instance.save()
    practitioner.role.connect(role_instance)
    role_instance.contracted_organization.connect(organization)
    process_role_locations(role_instance)
    process_role_networks(role_instance)
    process_prac_role_specialties(role_instance)
    log.debug(f"Practitioner created with element id {practitioner.element_id}")

def create_identifiers(prac: Practitioner):
    log.debug(f"About to create identifiers for practitioner {prac.first_name}")
    for rel_name, id_list in prac.get_pending_identifiers().items():
        rel = getattr(prac, rel_name)
        for id_node in id_list:
            if not hasattr(id_node, "element_id") or id_node.element_id is None:
                id_node.save()
            log.debug(f"Identifier saved to Aton its element id is: {id_node.element_id}")
            rel.connect(id_node)

def create_qualifications(prac: Practitioner):
    log.debug(
        f"Writing qualifications to Aton for Practitioner {prac.first_name} {prac.last_name}"
        f"Qualifications are: {prac.get_pending_qualifications()}"
    )
    rel = getattr(prac, "qualifications")
    for qual_node in prac.get_pending_qualifications():
        if not hasattr(qual_node, "element_id") or qual_node.element_id is None:
            qual_node.save()
            log.debug(f"Qualification saved to Aton its element id is: {qual_node.element_id}")
            rel.connect(qual_node)

def process_prac_role_specialties(role_instance: RoleInstance):
    log.debug(f"Processing specialties for the Practitioner:{role_instance.get_pending_prac_rs()}")
    for specialty in role_instance.get_pending_prac_rs():
        if not is_specialty_present(specialty.specialty, role_instance):
            log.debug(f"Specialty to be saved for the practitioner is {specialty.specialty}")
            log.debug(f"Primary specialty {specialty.isPrimary}")
            create_role_specialty(specialty, role_instance)
            if specialty.isPrimary == 'Y':
                role_instance.prac_primary_specialty.connect(specialty)

def is_specialty_present(specialty: str, role_instance: RoleInstance) -> bool:
    log.debug(f"About to check if specialty is present for {specialty}")
    for rel in role_instance.specialties:
        if rel.specialty == specialty:
            return True
    return False
