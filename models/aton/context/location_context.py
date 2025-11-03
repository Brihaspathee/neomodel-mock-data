import weakref

from models.aton.nodes.accessibility import Accessibility
from models.aton.nodes.identifier import LegacySystemIdentifier
from models.aton.nodes.location import Location
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.validation import Validation


class LocationContext:

    def __init__(self, location:Location):
        self.location = weakref.proxy(location)
        self._portico_source: LegacySystemIdentifier | None = None
        self._qualifications: list[Qualification] = []
        self._accessibility: Accessibility | None = None
        self._validation: Validation | None = None

    def set_portico_source(self, portico_source: LegacySystemIdentifier):
        self._portico_source = portico_source

    def get_portico_source(self) -> LegacySystemIdentifier:
        return self._portico_source

    def add_qualification(self, qualification: Qualification):
        self._qualifications.append(qualification)

    def get_qualifications(self) -> list[Qualification]:
        return self._qualifications

    def set_validation(self, validation: Validation):
        self._validation = validation

    def get_validation(self) -> Validation:
        return self._validation

    def set_accessibility(self, accessibility: Accessibility):
        self._accessibility = accessibility

    def get_accessibility(self) -> Accessibility:
        return self._accessibility