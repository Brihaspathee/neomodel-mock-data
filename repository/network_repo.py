from neomodel import DoesNotExist

from models.aton.nodes.network import Network


def find_network_by_code(code:str):
    try:
        network = Network.nodes.get(code=code)
        return network
    except DoesNotExist:
        return None