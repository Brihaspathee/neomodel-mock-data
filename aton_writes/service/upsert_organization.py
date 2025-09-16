import traceback
from typing import List, Tuple

from neomodel import db
from sqlalchemy.orm import relationship

from models.aton.nodes.contact import Contact
from models.aton.nodes.identifier import PPGID
from models.aton.nodes.organization import Organization
from aton_writes.service.upsert_role_instance import process_role_instance
from models.aton.nodes.pp_prov import PPProv
from models.aton.nodes.qualification import Qualification
from repository.contact_repo import create_contacts
from repository.organization_repo import get_organization_by_prov_id
import logging

log = logging.getLogger(__name__)

def upsert_organizations(organizations: list[Organization]):
    sorted_orgs = sorted(
        organizations,
        key=lambda org: (org.parent_ppg_id is not None, org.parent_ppg_id or "")
    )
    for organization in sorted_orgs:
        prov_id = organization.get_portico_source().prov_id
        existing_org = get_organization_by_prov_id(prov_id)
        if existing_org:
            # existing_org.name = organization.name
            update_organization(existing_org, organization, relationships=['qualifications'])
        else:
            create_organization(organization)

def create_organization(org: Organization):
    log.info(
        f"Writing organization {org.name} to Aton"
        f"Organization parent Id: {org.parent_ppg_id}"
    )
    try:
        log.info(org.__properties__)
        org.save()
        pp_prov: PPProv = org.get_portico_source().save()
        pp_prov.aton_org.connect(org)
        if org.parent_ppg_id is not None:
            log.info(f"Organization has parent {org.parent_ppg_id}")
            ppg = PPGID.nodes.get(value=org.parent_ppg_id)
            log.info(f"Parent PPG is {ppg}")
            parent_org = ppg.organization.single()
            log.info(f"Parent org is {parent_org.name}")
            if parent_org is not None:
                org.parent.connect(parent_org)
        log.debug(f"Organization written to Aton its id is: {org.element_id}")
        create_identifiers(org)
        # log.info(f"Pending Role instances:{org.get_pending_role_instances()}")
        create_qualifications(org)
        create_contacts(org)
        process_role_instance(org)
        return True
    except Exception as e:
        log.error(f"Error writing organization to Aton: {e}")
        log.debug(traceback.format_exc())
        raise


def create_identifiers(org):
    for rel_name, id_list in org.get_pending_identifiers().items():
        rel = getattr(org, rel_name)
        for id_node in id_list:
            if not hasattr(id_node, "element_id") or id_node.element_id is None:
                id_node.save()
                log.info(f"Identifier saved to Aton its element id is: {id_node.element_id}")
                rel.connect(id_node)


def create_qualifications(org: Organization):
    log.info(
        f"Writing qualifications to Aton for organization {org.name}"
        f"Qualifications are: {org.get_pending_qualifications()}"
    )
    rel = getattr(org, "qualifications")
    for qual_node in org.get_pending_qualifications():
        if not hasattr(qual_node, "element_id") or qual_node.element_id is None:
            qual_node.save()
            log.info(f"Qualification saved to Aton its element id is: {qual_node.element_id}")
            rel.connect(qual_node)

def update_organization(existing_org: Organization,
                        updated_org: Organization,
                        relationships: List[str]):
    log.info(
        f"Updating organization {existing_org.name} in Aton"
        f"Organization parent Id: {existing_org.parent_ppg_id}"
    )
    existing_org, changed = update_org_node_properties(existing_org, updated_org,relationships)
    if changed:
        existing_org.save()

def update_org_node_properties(existing_org: Organization,
                        updated_org: Organization, relationships: List[str]) -> Tuple[Organization, bool]:
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
                new_quals = updated_org.get_pending_qualifications()
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
                log.info(f"Existing quals: {existing_quals}")
                log.info(f"New quals: {new_quals}")
                for new_qual in new_quals:
                    qual_updated, is_new_qual = is_qual_updated(new_qual, existing_quals)
                    if is_new_qual:
                        new_qual.save()
                        log.info(f"Qualification saved to Aton its element id is: {new_qual.element_id}")
                        existing_org.qualifications.connect(new_qual)
                    # elif qual_updated:
                    #     existing_quals.remove(new_qual)
                    #     existing_quals.append(new_qual)
                    #     existing_quals.sort(key=lambda q: q.type)
                    #     existing_qual = existing_quals[0]
                    #     existing_qual.save()
    return existing_org, changed

def is_qual_updated(new_qual: Qualification, existing_quals: list[Qualification]) -> tuple[bool, bool]:
    qual_updated: bool = False
    is_new_qual: bool = True
    for existing_qual in existing_quals:
        if new_qual.type == existing_qual.type:
            # Compare the value, issuer and start date to see if a new one of the same type needs to be created
            if (new_qual.value != existing_qual.value or
                    new_qual.issuer != existing_qual.issuer or
                    new_qual.start_date != existing_qual.start_date):
                is_new_qual = True
            # if they are all the same, compare the end date to see if it needs to be updated
            elif new_qual.end_date != existing_qual.end_date:
                qual_updated = True
                existing_qual.end_date = new_qual.end_date
            return qual_updated,is_new_qual
    return qual_updated, is_new_qual



