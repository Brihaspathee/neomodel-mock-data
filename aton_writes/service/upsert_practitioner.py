

from aton_writes.service.upsert_role_location import process_role_locations
from aton_writes.service.upsert_role_network import process_role_networks
from aton_writes.service.upsert_role_specialty import create_role_specialty
from models.aton.nodes.identifier import LegacySystemID
from models.aton.nodes.organization import Organization
from models.aton.nodes.pp_prac import PP_PRAC
from models.aton.nodes.practitioner import Practitioner
from models.aton.nodes.role_instance import RoleInstance
from repository.practitioner_repo import get_practitioner_by_prac_id
from repository.role_instance_repo import get_role_instances
import logging

log = logging.getLogger(__name__)


def upsert_practitioner(organization: Organization):
    """
    Upserts practitioners to the given organization, ensuring pending practitioners
    are either updated or newly created along with their associated roles and connections.

    This function processes a list of pending practitioners for the provided organization.
    For each practitioner, it checks if they already exist by their unique identifier
    and either updates their associated role and connections or creates a new practitioner
    entry if none exists.

    :param organization: The organization object containing information about the
        organization to which practitioners will be upserted. It includes needed
        methods and attributes such as `name`, `element_id`, and the list of
        pending practitioners.
    :type organization: Organization
    :return: None
    """
    log.debug(f"About to upsert practitioners to organization {organization.name} with element id {organization.element_id}")
    for practitioner in organization.context.get_practitioners():
        log.debug(f"Practitioners is: {practitioner}")
        existing_prac = get_practitioner_by_prac_id(practitioner.context.get_portico_source().value)
        if existing_prac:
            log.debug(f"Practitioner already exists with element id {existing_prac.element_id}")
            role_instance = practitioner.context.get_role_instance()
            existing_ris = get_role_instances(existing_prac, organization)
            if not existing_ris:
                role_instance.save()
                existing_prac.role.connect(role_instance)
                role_instance.contracted_organization.connect(organization)
                process_role_locations(role_instance)
                process_role_networks(role_instance, organization.context)
                process_prac_role_specialties(role_instance)
        else:
            log.debug(f"Practitioner does not exist")
            create_practitioner(practitioner, organization)


def create_practitioner(practitioner: Practitioner, organization: Organization):
    """
    Creates a practitioner and associates it with an organization. This function handles saving the
    practitioner, creating identifiers, processing qualifications, and establishing connections between
    practitioner roles, locations, networks, and specialties. It ensures that the necessary components
    and relationships for the practitioner are properly set up within the system.

    :param practitioner: The Practitioner object to be created.
    :param organization: The Organization object to associate the practitioner with.
    :return: None
    """
    log.debug(f"About to create practitioner to organization {organization.name} with element id {organization.element_id}")
    practitioner.save()
    legacy_system_id: LegacySystemID = practitioner.context.get_portico_source()
    legacy_system_id.save()
    legacy_system_id.practitioner.connect(practitioner)
    pp_prac: PP_PRAC = PP_PRAC(prac_id=int(legacy_system_id.value))
    pp_prac.save()
    pp_prac.practitioner.connect(practitioner)
    create_identifiers(prac=practitioner)
    create_qualifications(prac=practitioner)
    role_instance: RoleInstance = practitioner.context.get_role_instance()
    log.debug(f"Pending Role Specialties: {role_instance.context.get_prac_rs()}")
    log.debug(f"Role instance is: {type(role_instance)}")
    role_instance.save()
    practitioner.role.connect(role_instance)
    role_instance.contracted_organization.connect(organization)
    process_role_locations(role_instance)
    process_role_networks(role_instance, organization.context)
    process_prac_role_specialties(role_instance)
    log.debug(f"Practitioner created with element id {practitioner.element_id}")


def create_identifiers(prac: Practitioner):
    """
    Creates and connects identifiers for a practitioner.

    This function retrieves the pending identifiers for the provided practitioner,
    saves them if they do not have an `element_id`, and establishes the necessary
    connections to the related nodes. The identifiers are logged after being saved.

    :param prac: The practitioner object for whom identifiers are to be created.
    :type prac: Practitioner

    :return: None
    """
    log.debug(f"About to create identifiers for practitioner {prac.first_name}")
    for rel_name, id_list in prac.context.get_identifiers().items():
        rel = getattr(prac, rel_name)
        for id_node in id_list:
            if not hasattr(id_node, "element_id") or id_node.element_id is None:
                id_node.save()
            log.debug(f"Identifier saved to Aton its element id is: {id_node.element_id}")
            rel.connect(id_node)


def create_qualifications(prac: Practitioner):
    """
    Writes pending qualifications of a practitioner to the respective external
    system and connects the qualifications to the practitioner entity.

    This function fetches the list of pending qualifications for a given
    `Practitioner` object, saves them to the external system, and establishes
    connections between the qualifications and the practitioner.

    :param prac: The practitioner for whom qualifications need to be processed.
    :type prac: Practitioner
    :return: None
    """
    log.debug(
        f"Writing qualifications to Aton for Practitioner {prac.first_name} {prac.last_name}"
        f"Qualifications are: {prac.context.get_qualifications()}"
    )
    rel = getattr(prac, "qualifications")
    for qual_node in prac.context.get_qualifications():
        if not hasattr(qual_node, "element_id") or qual_node.element_id is None:
            qual_node.save()
            log.debug(f"Qualification saved to Aton its element id is: {qual_node.element_id}")
            rel.connect(qual_node)


def process_prac_role_specialties(role_instance: RoleInstance):
    """
    Processes specialties associated with a practitioner role instance.

    This function evaluates the specialties waiting to be processed for the
    given role instance. If a specialty is not already associated with the
    role instance, it is saved and linked. For primary specialties, additional
    connections are established to associate it as the practitioner's primary
    specialty.

    :param role_instance: The practitioner role instance containing pending
        specialties to be processed.
    :type role_instance: RoleInstance
    """
    log.debug(f"Processing specialties for the Practitioner:{role_instance.context.get_prac_rs()}")
    for specialty in role_instance.context.get_prac_rs():
        if not is_specialty_present(specialty.specialty, role_instance):
            log.debug(f"Specialty to be saved for the practitioner is {specialty.specialty}")
            log.debug(f"Primary specialty {specialty.isPrimary}")
            create_role_specialty(specialty, role_instance)
            if specialty.isPrimary == 'Y':
                role_instance.prac_primary_specialty.connect(specialty)


def is_specialty_present(specialty: str, role_instance: RoleInstance) -> bool:
    """
    Checks whether the given specialty is present in the specialties of the
    provided `RoleInstance`.

    This function iterates over the specialties associated with the
    `RoleInstance` and checks if any of them match the given specialty string.

    :param specialty: The specialty string to check for.
    :param role_instance: The `RoleInstance` object that contains a collection
        of specialties to be searched.
    :return: A boolean value indicating whether the specialty is present.
    :rtype: bool
    """
    log.debug(f"About to check if specialty is present for {specialty}")
    for rel in role_instance.specialties:
        if rel.specialty == specialty:
            return True
    return False
