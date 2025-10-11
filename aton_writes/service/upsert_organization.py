import traceback
from typing import List, Tuple

from neomodel import db
from sqlalchemy.orm import relationship

from models.aton.nodes.contact import Contact
from models.aton.nodes.identifier import PPGID, LegacySystemID, TIN
from models.aton.nodes.organization import Organization
from aton_writes.service.upsert_role_instance import process_role_instance
from aton_writes.service.upsert_practitioner import upsert_practitioner
from models.aton.nodes.pp_prov import PP_PROV
from models.aton.nodes.qualification import Qualification
from repository.contact_repo import create_contacts
from repository.organization_repo import get_organization_by_prov_id
import logging

log = logging.getLogger(__name__)


def upsert_organizations(organizations: list[Organization]):
    """
    Inserts or updates a list of organizations in the database. The function first sorts
    the organizations by their parent hierarchy, ensuring that parent organizations are
    processed before their children. Each organization is then checked against the database
    to determine if it already exists based on its unique provider ID. If the organization
    exists, it is updated; otherwise, it is created.

    :param organizations: A list of Organization objects to be inserted or updated.
    :type organizations: list[Organization]
    :return: None
    """
    sorted_orgs = sorted(
        organizations,
        key=lambda org: (org.parent_ppg_id is not None, org.parent_ppg_id or "")
    )
    for organization in sorted_orgs:
        prov_id = organization.context.get_portico_source().value
        existing_org = get_organization_by_prov_id(prov_id)
        if existing_org:
            # existing_org.name = organization.name
            update_organization(existing_org, organization, relationships=['qualifications'])
        else:
            create_organization(organization)


def create_organization(org: Organization):
    """
    Create and save an organization instance to the database along with its identifiers,
    qualifications, contacts, and associated relationships. This includes connecting the
    organization to legacy system identifiers, parent organizations, and processing related
    practitioner and role instances. The function ensures all relationships and associated
    entities are created and properly persisted.

    :param org: The organization entity to be created and saved.
    :type org: Organization
    :return: True if the organization is successfully saved and processed.
    :rtype: bool
    :raises Exception: Raises an exception if there is an error during the organization
        creation and related processes.
    """
    log.debug(
        f"Writing organization {org.name} to Aton"
        f"Organization parent Id: {org.parent_ppg_id}"
    )
    try:
        log.debug(org.__properties__)
        org.save()
        legacySystemId: LegacySystemID = org.context.get_portico_source().save()
        legacySystemId.organization.connect(org)
        pp_prov:PP_PROV = PP_PROV(prov_id=int(legacySystemId.value))
        pp_prov.save()
        pp_prov.organization.connect(org)
        if org.parent_ppg_id is not None:
            log.debug(f"Organization has parent {org.parent_ppg_id}")
            ppg = PPGID.nodes.get(value=org.parent_ppg_id)
            log.debug(f"Parent PPG is {ppg}")
            parent_org = ppg.organization.single()
            log.debug(f"Parent org is {parent_org.name}")
            if parent_org is not None:
                org.parent.connect(parent_org)
        log.debug(f"Organization written to Aton its id is: {org.element_id}")
        create_identifiers(org)
        # log.debug(f"Pending Role instances:{org.get_pending_role_instances()}")
        create_qualifications(org)
        create_contacts(org)
        process_role_instance(org)
        upsert_practitioner(org)
        return True
    except Exception as e:
        log.error(f"Error writing organization to Aton: {e}")
        log.debug(traceback.format_exc())
        raise


def create_identifiers(org):
    """
    Creates and connects identifiers for the pending elements in the given organization.

    This function iterates over the pending identifiers of an organization, retrieves or
    creates identifiers if necessary, saves them, and connects them to the appropriate
    relationships within the organization.

    :param org: The organization containing pending identifiers.
    :type org: Organization
    :return: None
    """
    for rel_name, id_list in org.context.get_identifiers().items():
        rel = getattr(org, rel_name)
        for id_node in id_list:
            if not hasattr(id_node, "element_id") or id_node.element_id is None:
                if isinstance(id_node, TIN):
                    id_node, _ = id_node.get_or_create(
                        {"value": id_node.value},
                        {"legalName": id_node.legal_name},
                    )
                else:
                    id_node.save()
                log.debug(f"Identifier saved to Aton its element id is: {id_node.element_id}")
                rel.connect(id_node)


def create_qualifications(org: Organization):
    """
    Writes qualifications for an organization to a system.

    This function logs and processes pending qualifications for a given
    organization. It saves each qualification element if it does not have
    an element ID, logs the operation, and connects the qualification to
    the organization.

    :param org: Organization instance containing information about its
        qualifications.
    :type org: Organization
    :return: None
    """
    log.debug(
        f"Writing qualifications to Aton for organization {org.name}"
        f"Qualifications are: {org.context.get_qualifications()}"
    )
    rel = getattr(org, "qualifications")
    for qual_node in org.context.get_qualifications():
        if not hasattr(qual_node, "element_id") or qual_node.element_id is None:
            qual_node.save()
            log.debug(f"Qualification saved to Aton its element id is: {qual_node.element_id}")
            rel.connect(qual_node)


def update_organization(existing_org: Organization,
                        updated_org: Organization,
                        relationships: List[str]):
    """
    Updates the properties of an existing organization with the values from an updated
    organization instance, along with the specified relationships. Ensures that changes
    are saved if any updates have been made.

    This function logs the existing organization's name and parent organization ID (if available)
    before processing updates. It updates the provided organization instance's attributes
    based on changes detected and persists those changes if necessary.

    :param existing_org: The current organization instance that is to be updated.
    :type existing_org: Organization
    :param updated_org: The organization instance containing updated values to be applied
        to the existing instance.
    :type updated_org: Organization
    :param relationships: A list of relationship types that should also be updated as part
        of the organization update process.
    :type relationships: List[str]
    :return: The updated organization instance after applying changes and a boolean indicating
        whether any modifications were made (True if changes occurred, False otherwise).
    :rtype: Tuple[Organization, bool]
    """
    log.debug(
        f"Updating organization {existing_org.name} in Aton"
    )
    existing_org, changed = update_org_node_properties(existing_org, updated_org,relationships)
    if changed:
        existing_org.save()


def update_org_node_properties(existing_org: Organization,
                        updated_org: Organization, relationships: List[str]) -> Tuple[Organization, bool]:
    """
    Updates the properties and relationships of an existing organization node based on the
    provided updated organization node. Compares each property of the updated organization
    node with the corresponding property of the existing organization node and updates them
    if there are differences. For specific relationships, such as qualifications, additional
    processing is performed to update or connect the necessary relationships.

    :param existing_org: The existing Organization node in the database that needs to be updated.
    :param updated_org: The Organization node containing the updated values for properties
        and relationships.
    :param relationships: A list of relationship types to be updated. For example, "qualifications".
    :return: A tuple where the first element is the updated Organization node after modifications
        and the second is a boolean indicating whether any changes were made to its properties
        or relationships.

    :rtype: Tuple[Organization, bool]
    """
    changed: bool = False
    for prop in updated_org.__properties__:
        new_value = getattr(updated_org, prop, None)
        old_value = getattr(existing_org, prop, None)
        if new_value != old_value:
            setattr(existing_org, prop, new_value)
            changed = True

    if relationships:
        for rel in relationships:
            # Special case for qualifications
            if rel == "qualifications":
                new_quals = updated_org.context.get_qualifications()
                new_quals.sort(key=lambda q: q.type)
                query = """
                        MATCH (org:Organization)-[:HAS_QUALIFICATION]->(q)
                        WHERE elementId(org) = $org_id
                        RETURN q
                    """
                results, _ = db.cypher_query(query, {"org_id": existing_org.element_id})
                # Convert raw nodes to Neomodel objects
                existing_quals =  [Qualification.inflate(row[0]) for row in results]
                existing_quals.sort(key=lambda q: q.type)
                log.debug(f"Existing quals: {existing_quals}")
                log.debug(f"New quals: {new_quals}")
                for new_qual in new_quals:
                    is_qual_updated(new_qual, existing_quals, existing_org)
                    # if is_new_qual:
                    #     new_qual.save()
                    #     log.debug(f"Qualification saved to Aton its element id is: {new_qual.element_id}")
                    #     existing_org.qualifications.connect(new_qual)
                    # elif qual_updated:
                    #     new_qual.save()
                    #     existing_org.qualifications.connect(new_qual)
    return existing_org, changed


def is_qual_updated(new_qual: Qualification,
                    existing_quals: list[Qualification],
                    org:Organization) -> None:
    """
    Determines whether a new qualification (`new_qual`) needs to be saved and connected to an
    organization (`org`) based on its attributes and its relation to existing qualifications
    (`existing_quals`). It checks for updates or uniqueness among the qualifications provided.

    If `new_qual` has different attributes compared to an existing qualification of the same
    type, it is saved and connected to the organization. If the only difference is in the
    end date, and there are multiple qualifications of the same type, the most recent
    existing qualification is updated with the new end date. If `new_qual` is entirely new, it
    is saved and connected.

    The function does not return any value, and its primary side effect is modifying the
    database and/or the connections between qualifications and organizations.

    :param new_qual: The new qualification to be verified and potentially updated or added.
                     Its attributes are used for comparison with existing qualifications.
    :type new_qual: Qualification

    :param existing_quals: A list of existing qualifications to check against `new_qual`
                           for any updates or duplicates.
    :type existing_quals: list[Qualification]

    :param org: The organization with which the qualification is connected. It is used
                to associate the qualification upon addition or update.
    :type org: Organization

    :return: None
    :rtype: None
    """
    is_existing_qual = False
    same_type_existing_quals = []
    for existing_qual in existing_quals:
        if new_qual.type == existing_qual.type:
            is_existing_qual = True
            # Compare the value, issuer and start date to see if a new one of the same type needs to be created
            if (new_qual.value != existing_qual.value or
                    new_qual.issuer != existing_qual.issuer or
                    new_qual.start_date != existing_qual.start_date):
                new_qual.save()
                org.qualifications.connect(new_qual)
                return None
            # if they are all the same, add the qualification to the list of existing quals to compare with the end date
            elif new_qual.end_date != existing_qual.end_date:
                same_type_existing_quals.append(existing_qual)
    # If the qualification is an existing qualification, then if something was changed,
    # it was immediately saves and returned. If only the end date was changed, then
    # it is added to the list of existing quals to compare with the end date. If
    # nothing has changed, then no update is needed for the qualification.
    if not is_existing_qual:
        # If it is not an existing qualification, then create a new one.
        new_qual.save()
        org.qualifications.connect(new_qual)
    elif len(same_type_existing_quals) > 0:
        # if it is an existing qualification, then compare the end date with the existing ones of the same type.
        # retrieve the latest qualification of the same type and update its end date.
        latest_qual = max(same_type_existing_quals, key=lambda o: o.end_date)
        latest_qual.end_date = new_qual.end_date
        latest_qual.save()
    return None



