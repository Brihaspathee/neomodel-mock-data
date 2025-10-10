import logging

from models.aton.context.contact_context import ContactContext
from models.aton.context.role_instance_context import RoleInstanceContext
from models.aton.context.role_location_context import RoleLocationContext
from models.aton.nodes.contact import Contact
from models.aton.nodes.hours_of_operation import HoursOfOperation
from models.aton.nodes.telecom import Telecom
from transform.transform_utils import set_location
from utils.location_util import get_hash_key_for_prov_tin_loc
from models.aton.nodes.organization import Organization
from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.role_location import RoleLocation
from models.portico import PPProv, PPProvTinLoc, PPProvLocOfHours
from transform.transform_provider_net_cycle import transform_provider_net_cycle
from transform.attributes.transform_attribute import transform_attributes
from utils.office_hours import format_office_hours

log = logging.getLogger(__name__)

def transform_provider_location(provider: PPProv, organization:Organization):
    """
    Transforms provider location based on the given provider and organization.
    This function processes the provider's locations and networks, updates the
    corresponding role instance, and adds it to the organization.

    :param provider: The provider containing location and network information
    :param organization: The organization to which the transformed role instance
        will be added
    :return: None
    """
    if provider.prov_locs or provider.networks:
        # ------------------------------------------------------------------------------
        # When there are any locations or networks directly associated with the provider,
        # then a RoleInstance node should be created with the role type "HAS_ROLE"
        # ------------------------------------------------------------------------------
        log.debug("Transforming Portico Provider Location")
        role_instance: RoleInstance = RoleInstance()
        role_instance.context = RoleInstanceContext(role_instance)
        role_instance.context.set_role_type("has_role")
        if provider.prov_locs:
            # ------------------------------------------------------------------------------
            # Process the provider locations
            # ------------------------------------------------------------------------------
            _process_prov_locs(provider, role_instance)
        if provider.networks:
            # ------------------------------------------------------------------------------
            # Process the provider networks
            # ------------------------------------------------------------------------------
            log.debug("Transforming Portico Provider Network")
            transform_provider_net_cycle(provider.networks, role_instance)
        # ------------------------------------------------------------------------------
        # Add the role instance to the organization
        # ------------------------------------------------------------------------------
        organization.context.add_role_instance(role_instance)

def _process_prov_locs(pp_prov:PPProv, role_instance: RoleInstance):
    """
    Processes a list of provider locations and associates them with a role instance.

    This function iterates through the provided list of provider locations, creating
    an instance of `RoleLocation` for each, and sets the location details using a
    hash key generated from the provider's location details. The resulting
    `RoleLocation` objects are associated with the provided role instance. Logging is
    performed to provide insights into key operation points such as the processed
    addresses and generated hash codes.

    :param prov_locs:
        A list of `PPProvLoc` objects representing the provider locations to process.
    :param role_instance:
        An instance of `RoleInstance` where the processed role locations should
        be associated.
    :return:
        This function does not return a value.
    """
    for prov_loc in pp_prov.prov_locs:
        # ------------------------------------------------------------------------------
        # Create a new RoleLocation instance for each provider location
        # Set the location details using a hash key generated from the provider's location details'
        # Add the role location to the role instance
        # ------------------------------------------------------------------------------
        role_location: RoleLocation = RoleLocation()
        role_location.context = RoleLocationContext(role_location)
        if prov_loc.PRIMARY == "Y":
            role_location.context.set_is_primary(True)
        prov_tin_loc: PPProvTinLoc = prov_loc.location
        log.debug(f"Location Address:{prov_tin_loc.address}")
        hash_code = get_hash_key_for_prov_tin_loc(prov_tin_loc=prov_tin_loc)
        log.debug(f"Hash Code:{hash_code}")
        location = set_location(hash_code, prov_tin_loc)
        role_location.context.set_location(location)
        contact: Contact = get_location_phone(prov_tin_loc)
        transform_attributes("PROV_LOC", pp_prov, prov_tin_loc, role_location)
        role_location.context.add_contact(contact)
        get_prov_loc_office_hours(pp_prov, prov_tin_loc, role_location)
        role_instance.context.add_rl(role_location)
        log_role_location_contacts(role_location=role_location)


def get_location_phone(pp_prov_tin_loc:PPProvTinLoc) -> Contact:
    contact: Contact = Contact()
    contact.context = ContactContext(contact)
    contact.use = "Directory"
    if pp_prov_tin_loc.address:
        loc_address = pp_prov_tin_loc.address
        if loc_address.phones:
            telecom: Telecom = Telecom()
            for addr_phone in loc_address.phones:
                log.debug(f"Location phone is {addr_phone}")
                log.debug(f"Location phone is {addr_phone.phone}")
                if addr_phone.phone.type == "PHONE":
                    telecom.phone = addr_phone.phone.areacode + addr_phone.phone.exchange + addr_phone.phone.num
                elif addr_phone.phone.type == "FAX":
                    telecom.fax = addr_phone.phone.areacode + addr_phone.phone.exchange + addr_phone.phone.num
                elif addr_phone.phone.type == "TTY":
                    telecom.tty = addr_phone.phone.areacode + addr_phone.phone.exchange + addr_phone.phone.num
                elif addr_phone.phone.type == "AFH":
                    telecom.afterHoursNumber = addr_phone.phone.areacode + addr_phone.phone.exchange + addr_phone.phone.num
            contact.context.set_telecom(telecom)
    return contact

def get_prov_loc_office_hours(provider:PPProv, pp_prov_tin_loc:PPProvTinLoc, role_location:RoleLocation):
    # converted_office_hours = format_office_hours(prov_loc_office_hours=provider.loc_ofhours)
    # log.error(f"Converted office hours - {converted_office_hours}")
    prov_loc_office_hours: list[PPProvLocOfHours] = []
    for prov_loc_ofhours in provider.loc_ofhours:
        location: PPProvTinLoc = prov_loc_ofhours.location
        if location.id == pp_prov_tin_loc.id:
            prov_loc_office_hours.append(prov_loc_ofhours)
    converted_office_hours = format_office_hours(prov_loc_office_hours=prov_loc_office_hours)
    log.debug(f"Converted office hours - {converted_office_hours}")
    if not converted_office_hours:
        return
    is_office_hours_set = False
    if role_location.context.get_contacts():
        for contact in role_location.context.get_contacts():
            if contact.use == "Directory":
                hours_of_operation: HoursOfOperation = HoursOfOperation(hours=converted_office_hours)
                contact.context.set_hours_of_operation(hours_of_operation)
                is_office_hours_set = True
                break
    if not is_office_hours_set:
        contact: Contact = Contact()
        contact.use = "Directory"
        hours_of_operation: HoursOfOperation = HoursOfOperation(hours=converted_office_hours)
        contact.context.set_hours_of_operation(hours_of_operation)
        role_location.context.add_contact(contact)

def log_role_location_contacts(role_location: RoleLocation):
    if role_location.context.get_contacts():
        for contact in role_location.context.get_contacts():
            log.debug(f"Contact: {contact}")
            log.debug(f"Contact Use: {contact.use}")
            log.debug(f"Contact Hours of operation: {contact.context.get_hours_of_operation()}")





