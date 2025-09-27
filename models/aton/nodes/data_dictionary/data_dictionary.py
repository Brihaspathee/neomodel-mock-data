from neomodel import StructuredNode, StringProperty, RelationshipTo

from models.aton.nodes.specialty import Specialty


class DataDictionary(StructuredNode):
    definition: str = StringProperty(required=True)

    specialty = RelationshipTo('Specialty', 'SPECIALTIES_DEFINED')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pending_specialty: Specialty | None = None

    def set_specialty(self, specialty: Specialty):
        self._pending_specialty = specialty

    def get_specialty(self):
        return self._pending_specialty
