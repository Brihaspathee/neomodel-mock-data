from models.aton.organization import Organization
from aton_writes.service.upsert_product import create_product
import logging

from models.aton.product import Product
from models.aton.role_instance import RoleInstance

log = logging.getLogger(__name__)


def write_to_aton(org: Organization):
    log.debug(
        f"Writing organization {org.name} to Aton"
    )
    try:
        log.info(org.__properties__)
        org.save()
        log.debug(f"Organization written to Aton its id is: {org.element_id}")
        for rel_name, id_list in org._pending_identifiers.items():
            rel = getattr(org, rel_name)
            for id_node in id_list:
                if not hasattr(id_node, "element_id") or id_node.element_id is None:
                    id_node.save()
                    log.info(f"Identifier saved to Aton its element id is: {id_node.element_id}")
                    rel.connect(id_node)
        log.info(f"Pending Role instances:{org._pending_role_instances}")
        for role_type, role_instance_list in org._pending_role_instances.items():
            if role_type == "has_role":
                for role_instance in role_instance_list:
                    role_instance.save()
                    log.info(f"Role instance saved to Aton its element id is: {role_instance.element_id}")
                    org.role.connect(role_instance)
            # elif role_type == "contracted_by":
            #     for role_instance in role_instance_list:
            #         role_instance.save()
            #         log.info(f"Role instance saved to Aton its element id is: {role_instance.element_id}")
            #         org.contracted_by.connect(role_instance)
        return True
    except Exception as e:
        log.error(f"Error writing organization to Aton: {e}")
        return False

def write_products_networks(product: Product):
    create_product(product)