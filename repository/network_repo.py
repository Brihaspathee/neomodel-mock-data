from neomodel import DoesNotExist

from models.aton.nodes.network import Network
from models.aton.nodes.pp_net import PPNet


def find_network_by_code(code: str):
    try:
        return Network.nodes.get(code=code)
    except DoesNotExist:
        pass

    try:
        return PPNet.nodes.get(net_id=code).sources.single()
    except DoesNotExist:
        return None

def find_network_by_code_or_name(code: str, name: str) -> tuple[Network | None, bool]:
    is_network_found_by_name = False
    try:
        return Network.nodes.get(code=code), is_network_found_by_name
    except DoesNotExist:
        pass
    try:
        product = Network.nodes.get(name=name)
        is_network_found_by_name = True
        return product, True
    except DoesNotExist:
        return None, is_network_found_by_name