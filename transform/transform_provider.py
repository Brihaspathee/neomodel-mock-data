from models.aton.nodes.contact import Contact
from models.aton.nodes.identifier import TIN
from models.aton.nodes.organization import Organization
from transform.transformers import transform_to_aton
from transform.transform_provider_location import transform_provider_location
from transform.transform_attribute import get_provider_attributes
import logging

from models.portico import PPProv

log = logging.getLogger(__name__)

@transform_to_aton.register(PPProv)
def _(provider:PPProv) -> Organization:
    """
    Transforms a PPProv provider instance into an Organization instance.

    :param provider: The PPProv provider instance to be transformed.
    :type provider: PPProv
    :return: A new Organization instance created from the provided PPProv data.
    :rtype: Organization
    """
    log.info("Transforming Portico Provider")
    # ------------------------------------------------------------------------------
    # Populate basic details of an Organization
    # ------------------------------------------------------------------------------
    organization = Organization(name=provider.name)
    organization.description = provider.name
    organization.type = provider.prov_type.type
    organization.capitated = False
    organization.pcp_practitioner_required = False
    organization.atypical = False
    tax_id: TIN = get_tin(provider)
    log.info(f"TIN is {tax_id}")
    organization.add_identifier(tax_id)
    get_provider_address(provider)
    get_provider_attributes(provider, organization)
    # ------------------------------------------------------------------------------
    # Populate locations associated with the organization
    # ------------------------------------------------------------------------------
    transform_provider_location(provider, organization)
    return organization

def get_tin(provider:PPProv) -> TIN:
    """
    Generates a TIN (Taxpayer Identification Number) from the provided provider's
    information. This function retrieves the TIN value and legal name associated
    with the provider and constructs a TIN instance.

    :param provider: The provider instance containing the TIN data.
    :type provider: PPProv
    :return: A TIN instance containing the taxpayer identification number and
        associated legal name.
    :rtype: TIN
    """
    tin: TIN = TIN(value= provider.tin.tin,
                   legal_name = provider.tin.name)
    return tin

def get_provider_address(provider:PPProv) -> Contact:
    for address in provider.address:
        log.info(f"Provider Address is {address}")