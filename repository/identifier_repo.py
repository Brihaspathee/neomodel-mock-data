from models.aton.nodes.identifier import MedicaidID, TIN

import logging
log = logging.getLogger(__name__)

def create_identifiers(owner_node):
    """
    Creates and assigns unique identifiers to nodes in the owner's context and connects
    them to the appropriate relationships. Identifiers may be created or updated depending
    on the node type and its existing attributes.

    :param owner_node: The parent node containing relationships and context for generating
        identifiers.
    :type owner_node: Any
    :return: None
    """
    for rel_name, id_list in owner_node.context.get_identifiers().items():
        rel = getattr(owner_node, rel_name)
        for id_node in id_list:
            if not hasattr(id_node, "element_id") or id_node.element_id is None:
                if isinstance(id_node, TIN):
                    log.info(f"TIN Node:{id_node}")
                    id_node, _ = id_node.get_or_create(
                        {"value": id_node.value},
                        {"legal_name": id_node.legal_name},
                    )
                elif isinstance(id_node, MedicaidID):
                    id_node, _ = id_node.get_or_create(
                        {"value": id_node.value, "state": id_node.state},
                        {"start_date": id_node.start_date, "end_date": id_node.end_date},
                    )
                else:
                    id_node.save()
            log.debug(f"Identifier saved to Aton its element id is: {id_node.element_id}")
            rel.connect(id_node)