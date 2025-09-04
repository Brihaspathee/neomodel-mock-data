from sqlalchemy import alias

from models.aton.identifier import Identifier, TIN
from models.aton.organization import Organization
from transform.transformers import transform_to_aton
from transform.transform_provider_location import transform_provider_location
import logging

from models.portico import PPProv

log = logging.getLogger(__name__)

@transform_to_aton.register(PPProv)
def _(provider:PPProv) -> Organization:
    log.info("Transforming Portico Provider")
    organization = Organization(name=provider.name)
    organization.description = provider.name
    organization.type = provider.prov_type.type
    organization.capitated = False
    organization.pcp_practitioner_required = False
    organization.atypical = False
    tax_id: TIN = get_tin(provider)
    log.info(f"TIN is {tax_id}")
    organization.add_identifier(tax_id)
    transform_provider_location(provider, organization)
    return organization

def get_tin(provider:PPProv) -> TIN:
    tin: TIN = TIN(value= provider.tin.tin,
                   legal_name = provider.tin.name)
    return tin