from neomodel import StructuredNode, StringProperty, RelationshipTo
from neomodel.exceptions import DoesNotExist

from models.aton.nodes.specialty_classification import SpecialtyClassification


class SpecialtyGroup(StructuredNode):
    name: str = StringProperty(required=True)

    classifications = RelationshipTo('SpecialtyClassification', 'CLASSIFIED_BY')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pending_classifications: list[SpecialtyClassification] = []

    def add_classification(self, classification: SpecialtyClassification):
        self._pending_classifications.append(classification)

    def get_classifications(self):
        return self._pending_classifications

    @classmethod
    def get_or_create(cls, instance: "SpecialtyGroup") -> tuple["SpecialtyGroup", bool]:
        try:
            node = cls.nodes.get(name=instance.name)
            created = False
        except DoesNotExist:
            node = cls(name=instance.name).save()
            created = True

        node._pending_groups = instance.get_classifications()
        return node, created