from neomodel import StructuredNode, StringProperty, RelationshipTo

from models.aton.nodes.data_dictionary.specialty_type import SpecialtyType


class DataDictionary(StructuredNode):
    definition: str = StringProperty(required=True)

    specialty = RelationshipTo('models.aton.nodes.data_dictionary.specialty_type', 'SPECIALTIES_DEFINED')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pending_specialty: SpecialtyType | None = None

    def set_specialty(self, specialty: SpecialtyType):
        self._pending_specialty = specialty

    def get_specialty(self):
        return self._pending_specialty
