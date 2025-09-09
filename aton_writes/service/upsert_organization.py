import traceback

from models.aton.nodes.contact import Contact
from models.aton.nodes.identifier import PPGID
from models.aton.nodes.organization import Organization
from aton_writes.service.upsert_role_instance import process_role_instance
from repository.contact_repo import create_contacts
import logging

log = logging.getLogger(__name__)


def create_organization(org: Organization):
    log.info(
        f"Writing organization {org.name} to Aton"
        f"Organization parent Id: {org.parent_ppg_id}"
    )
    try:
        log.info(org.__properties__)
        org.save()
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