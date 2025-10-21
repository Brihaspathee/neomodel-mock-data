from models.aton.context.contact_context import ContactContext
from models.aton.nodes.address import Address
from models.aton.nodes.contact import Contact
from models.aton.nodes.identifier import TIN, LegacySystemIdentifier
from models.aton.nodes.organization import Organization
from models.aton.context.organization_context import OrganizationContext
from models.aton.nodes.telecom import Telecom
from transform.qualification_deduplication import select_unique_qualifications
from transform.transformers import transform_to_aton
from transform.transform_provider_location import transform_provider_location
from transform.transform_practitioner import transform_practitioner
from transform.attributes.transform_attribute import transform_attributes
import logging

from models.portico import PPProv
from utils.address_util import portico_address_to_aton
from config.contact_settings import ADDRESS_USE_MAPPING

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
    log.debug("Transforming Portico Provider")
    # ------------------------------------------------------------------------------
    # Populate basic details of an Organization
    # ------------------------------------------------------------------------------
    # organization = get_organization_by_prov_id(str(provider.id))
    # if not organization:
    organization = Organization(name=provider.name)
    organization.context = OrganizationContext(organization)
    pp_prov: LegacySystemIdentifier = LegacySystemIdentifier(value=str(provider.id),
                                                             system="PORTICO",
                                                             systemIdType="PROV ID")
    organization.context.set_portico_source(pp_prov)
    organization.alias = provider.name
    organization.description = provider.name
    organization.type = provider.prov_type.type_ds
    organization.capitated = False
    organization.pcp_practitioner_required = False
    organization.atypical = False
    tax_id: TIN = get_tin(provider)
    log.debug(f"TIN is {tax_id}")
    organization.context.add_identifier(tax_id)
    contact: Contact = get_provider_address(provider)
    organization.context.add_contact(contact)
    # ------------------------------------------------------------------------------
    # Populate locations associated with the organization
    # ------------------------------------------------------------------------------
    transform_provider_location(provider, organization)
    transform_attributes("PROVIDER", provider, organization)
    # ------------------------------------------------------------------------------
    # Add the practitioners associated with the organization
    # ------------------------------------------------------------------------------
    transform_practitioner(provider, organization)
    if organization.context.get_qualifications():
        qual_results = select_unique_qualifications(organization.context.get_qualifications())
        log.info(qual_results)
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
    contact: Contact = Contact()
    contact.context = ContactContext(contact)
    for pp_address in provider.addresses:
        log.debug(f"Provider Address is {pp_address}")
        log.debug(f"Provider Address is {pp_address.address}")
        address: Address = portico_address_to_aton(pp_address.address)
        contact_use = ADDRESS_USE_MAPPING.get(pp_address.address.type)
        if contact_use:
            contact.use = contact_use
        else:
            log.warning(
                f"Unknown address type {pp_address.address.type} for provider {provider.name}"
            )
        contact.context.set_address(address)
        if pp_address.address.phones:
            telecom: Telecom = Telecom()
            for addr_phone in pp_address.address.phones:
                log.debug(f"Address phone is {addr_phone}")
                log.debug(f"Address phone is {addr_phone.phone}")
                if addr_phone.phone.type == "PHONE":
                    telecom.phone = addr_phone.phone.areacode + addr_phone.phone.exchange + addr_phone.phone.num
                elif addr_phone.phone.type == "FAX":
                    telecom.fax = addr_phone.phone.areacode + addr_phone.phone.exchange + addr_phone.phone.num
                elif addr_phone.phone.type == "TTY":
                    telecom.tty = addr_phone.phone.areacode + addr_phone.phone.exchange + addr_phone.phone.num
                elif addr_phone.phone.type == "AFH":
                    telecom.afterHoursNumber = addr_phone.phone.areacode + addr_phone.phone.exchange + addr_phone.phone.num
                else:
                    log.warning(
                        f"Unknown phone type {addr_phone.phone.type} for provider {provider.name}"
                    )
            contact.context.set_telecom(telecom)
    return contact

# def compare_and_update_properties(provider:PPProv, organization:Organization):
#     log.debug(f"provider alais name in Portico is {provider.name}")
#     log.debug(f"organization type is {provider.prov_type.type}")
#     organization.name = provider.name