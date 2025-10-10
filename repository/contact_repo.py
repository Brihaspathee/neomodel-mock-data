from typing import Any

from models.aton.nodes.contact import Contact
import logging

log = logging.getLogger(__name__)

def create_contacts(contact_owner:Any):
    log.debug(
        f"Writing contacts"
        f"Contacts are: {contact_owner.context.get_contacts()}"
    )
    rel = getattr(contact_owner, "contacts")
    for contact in contact_owner.context.get_contacts():
        if not hasattr(contact, "element_id") or contact.element_id is None:
            contact.save()
            log.debug(f"Contact saved to Aton its element id is: {contact.element_id}")
            rel.connect(contact)
            create_address(contact)
            create_telecom(contact)
            create_hours_of_operation(contact)

def create_address(contact: Contact):
    rel = getattr(contact, "address")
    if contact.get_pending_address() is not None:
        address = contact.get_pending_address()
        if not hasattr(address, "element_id") or address.element_id is None:
            address.save()
            log.debug(f"Address saved to Aton its element id is: {address.element_id}")
            rel.connect(address)

def create_telecom(contact: Contact):
    rel = getattr(contact, "telecom")
    if contact.get_pending_telecom() is not None:
        telecom = contact.get_pending_telecom()
        if not hasattr(telecom, "element_id") or telecom.element_id is None:
            telecom.save()
            log.debug(f"Telecom saved to Aton its element id is: {telecom.element_id}")
            rel.connect(telecom)

def create_hours_of_operation(contact: Contact):
    rel = getattr(contact, "hours_of_operation")
    if contact.get_pending_hours_of_operation() is not None:
        hours_of_operation = contact.get_pending_hours_of_operation()
        if not hasattr(hours_of_operation, "element_id") or hours_of_operation.element_id is None:
            hours_of_operation.save()
            log.debug(f"Hours of operation saved to Aton its element id is: {hours_of_operation.element_id}")
            rel.connect(hours_of_operation)