import logging
from functools import singledispatch

from models.aton.organization import Organization
from models.portico import PPProv

log = logging.getLogger(__name__)

def transformer(portico_entity_list) -> list | None:
    log.info("Transformer")
    organizations: list[Organization] = []
    is_org: bool = False
    for porticoEntity in portico_entity_list:
        if isinstance(porticoEntity,PPProv):
            is_org = True
            organization: Organization = transform_to_aton(porticoEntity)
        if is_org:
            organizations.append(organization)
    if organizations:
        return organizations
    else:
        return None

@singledispatch
def transform_to_aton(arg):
    raise TypeError(f"{arg} is not a valid Portico type")