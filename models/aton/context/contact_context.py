import weakref

from models.aton.nodes.address import Address
from models.aton.nodes.contact import Contact
from models.aton.nodes.hours_of_operation import HoursOfOperation
from models.aton.nodes.telecom import Telecom


class ContactContext:

    def __init__(self, contact:Contact):
        self.contact = weakref.proxy(contact)
        self._address: Address | None = None
        self._telecom: Telecom | None = None
        self._hours_of_operation: HoursOfOperation | None = None

    def set_address(self, address: Address):
        self._address = address

    def get_address(self):
        return self._address

    def set_telecom(self, telecom: Telecom):
        self._telecom = telecom

    def get_telecom(self):
        return self._telecom

    def set_hours_of_operation(self, hours_of_operation: HoursOfOperation):
        self._hours_of_operation = hours_of_operation

    def get_hours_of_operation(self):
        return self._hours_of_operation