import logging
log = logging.getLogger(__name__)

def transform_hat_code_attr(**kwargs):
    prov_attrib = kwargs.get("prov_attrib")
    org = kwargs.get("organization")
    log.debug("Transforming hat code attribute")
    for value in prov_attrib.values:
        log.debug(f"Value: {value}")
        log.debug(f"Value: {value.value}")
        log.debug(f"Role Instances: {type(org.context.get_role_instances())}")
        for role, role_instances in org.context.get_role_instances().items():
            log.debug(f"Role: {role}")
            if role == "has_role":
                for role_instance in role_instances:
                    log.debug(f"Role Networks: {role_instance.context.get_rns()}")
                    for role_network in role_instance.context.get_rns():
                        if value.value == "PS":
                            role_network.context.set_is_pcp(True)
                            role_network.context.set_is_specialist(True)
                        elif value.value == "SP":
                            role_network.context.set_is_specialist(True)
                        elif value.value == "PC":
                            role_network.context.set_is_pcp(True)
                        elif value.value == "BH":
                            role_network.context.set_is_behavior_health(True)