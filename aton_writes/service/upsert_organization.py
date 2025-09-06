from models.aton.nodes.organization import Organization
from aton_writes.service.upsert_role_instance import process_role_instance
import logging

log = logging.getLogger(__name__)


def create_organization(org: Organization):
    log.debug(
        f"Writing organization {org.name} to Aton"
    )
    try:
        log.info(org.__properties__)
        org.save()
        log.debug(f"Organization written to Aton its id is: {org.element_id}")
        for rel_name, id_list in org.get_pending_identifiers().items():
            rel = getattr(org, rel_name)
            for id_node in id_list:
                if not hasattr(id_node, "element_id") or id_node.element_id is None:
                    id_node.save()
                    log.info(f"Identifier saved to Aton its element id is: {id_node.element_id}")
                    rel.connect(id_node)
        log.info(f"Pending Role instances:{org.get_pending_role_instances()}")
        process_role_instance(org)
        return True
    except Exception as e:
        log.error(f"Error writing organization to Aton: {e}")
        return False