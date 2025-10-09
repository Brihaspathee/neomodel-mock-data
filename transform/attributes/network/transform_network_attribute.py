from config.attribute_settings import ATTRIBUTES_CONFIG
from models.aton.nodes.network import Network
from models.portico.pp_net import PPNetDict

import logging
from typing import Any

log = logging.getLogger(__name__)

def get_net_attributes(pp_net:PPNetDict, network:Network):
    log.debug(f"Network type: {type(pp_net)}")
    log.debug(f"Network Attributes: {pp_net.get('attributes')}")
    for attribute in pp_net.get('attributes', []):
        log.debug(f"Attribute: {attribute.get('attribute_id')}")
        try:
            attr_mapping = ATTRIBUTES_CONFIG["network"][attribute.get('attribute_id')]
            # Load the attribute only if a mapping is present
            # else do not load the attribute
            attribute_fields: dict[str, Any] = {}
            for value in attribute.get("values", []):
                field_id = str(value.get("field_id"))
                attribute_fields[field_id] = value.get("value")
                if attribute.get("attribute_type") == "NET_IS_VENDOR" and value.get("value") == "Y":
                    network.isVendorNetwork = True
                elif attribute.get("attribute_type") == "NET_HEALTHNET" and value.get("value") == "Y":
                    network.isHNETNetwork = True
        except KeyError:
            log.debug(f"No mapping found for attribute {attribute.get('attribute_id')}, hence it will not be loaded")