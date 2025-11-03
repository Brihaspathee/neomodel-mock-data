from models.aton.nodes.network import Network
from models.aton.context.organization_context import OrganizationContext
from models.aton.nodes.node_utils import update_relationship_dates
from models.aton.nodes.role_instance import RoleInstance
import logging

from models.aton.relationships.has_panel import HasPanel
from utils.location_util import get_hash_key_for_location

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
    for rn in role_instance.context.get_rns():
        rn.save()
        network: Network = rn.context.get_network()
        rn.network.connect(network)
        role_instance.role_networks.connect(rn)
        # organization = role_instance.organization.single()
        # if organization:
        #     log.info(f"The org associated with this role instance is: {organization.name}")
        if org_context:
            log.debug(f"The organization has context: {org_context}")
        for assoc_rl in rn.context.get_assoc_rls():
            rl = assoc_rl.role_location
            log.debug(f"Role Location inside the network:{rl.element_id}")
            for rls in assoc_rl.rls_edges:
                rel = rl.role_network.connect(rn, {
                    "start_date": rls.start_date,
                    "end_date": rls.end_date
                })
                log.debug(f"RLS element id:{rel.element_id}")
                update_relationship_dates(rel, rls.start_date, rls.end_date)
            panel_edge = assoc_rl.panel_edge
            if panel_edge:
                rl.rn_has_panel.connect(rn, panel_edge.__properties__)
            if rn.context.get_is_pcp():
                log.debug(f"Create IS_PCP edge between role network node with element id {rl.element_id} "
                         f"and role network node with element id {rn.element_id}")
                rl.rn_pcp.connect(rn)
            if rn.context.get_is_specialist():
                log.debug(f"Create IS_SPECIALIST edge between role network node with element id {rl.element_id} "
                         f"and role network node with element id {rn.element_id}")
                rl.rn_specialist.connect(rn)
            if rn.context.get_is_behavior_health():
                log.debug(f"Create IS_BEHAVIORAL_HEALTH edge between role network node with element id {rl.element_id} "
                         f"and role network node with element id {rn.element_id}")
                rl.rn_behavior_health.connect(rn)
            # if rn.context.get_panel():
            #
            #     has_panel:HasPanel = rn.context.get_panel().panel_edge
            #     panel_rl = rn.context.get_panel().role_location
            #     panel_loc_hash_code = get_hash_key_for_location(location=panel_rl.context.get_location())
            #     rl_has_code = get_hash_key_for_location(location=rl.context.get_location())
            #     if panel_loc_hash_code == rl_has_code:
            #         log.info(f"Create HAS_PANEL edge between role network node with element id {rl.element_id} "
            #                  f"and role network node with element id {rn.element_id}")
            #         # rl.rn_has_panel.connect(rn, {
            #         #     "status": has_panel.status,
            #         #     "gender_limitation": has_panel.gender_limitation
            #         # }),
            #         rl.rn_has_panel.connect(rn, has_panel.__properties__)
