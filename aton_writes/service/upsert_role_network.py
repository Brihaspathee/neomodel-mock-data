from models.aton.nodes.network import Network
from models.aton.context.organization_context import OrganizationContext
from models.aton.nodes.role_instance import RoleInstance
import logging

log = logging.getLogger(__name__)


def process_role_networks(role_instance:RoleInstance,
                          org_context: OrganizationContext):
    """
    Processes the pending role networks and their associated role locations for the
    specified role instance. This includes saving pending role networks, connecting
    them to the appropriate network and role networks, and processing their
    associated role locations by connecting them with the relevant role network.

    :param role_instance: The role instance object whose pending role networks and
        associated role locations are to be processed.
    :type role_instance: RoleInstance
    :return: None
    """
    log.debug("Coming inside process role networks")
    for rn in role_instance.get_pending_rns():
        rn.save()
        network: Network = rn.get_network()
        rn.network.connect(network)
        role_instance.role_networks.connect(rn)
        # organization = role_instance.organization.single()
        # if organization:
        #     log.info(f"The org associated with this role instance is: {organization.name}")
        if org_context:
            log.debug(f"The organization has context: {org_context}")
        for assoc_rl in rn.get_pending_assoc_rls():
            rl = assoc_rl.role_location
            log.debug(f"Role Location inside the network:{rl.element_id}")
            for rls in assoc_rl.rls_edges:
                rl.role_network.connect(rn, {
                    "start_date": rls.start_date,
                    "end_date": rls.end_date
                })
            if rn.get_is_pcp():
                log.debug(f"Create IS_PCP edge between role network node with element id {rl.element_id} "
                         f"and role network node with element id {rn.element_id}")
                rl.rn_pcp.connect(rn)
            if rn.get_is_specialist():
                log.debug(f"Create IS_SPECIALIST edge between role network node with element id {rl.element_id} "
                         f"and role network node with element id {rn.element_id}")
                rl.rn_specialist.connect(rn)
            if rn.get_is_behavior_health():
                log.debug(f"Create IS_BEHAVIORAL_HEALTH edge between role network node with element id {rl.element_id} "
                         f"and role network node with element id {rn.element_id}")
                rl.rn_behavior_health.connect(rn)