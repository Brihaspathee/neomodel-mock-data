from neomodel import StructuredNode, StringProperty, RelationshipTo
from neomodel.exceptions import DoesNotExist

from models.aton.nodes.dd_specialty import DD_Specialty
from models.data_classes.specialtytype import Specialization


class SpecialtyClassification(StructuredNode):
    name: str = StringProperty(required=True)

    specialties = RelationshipTo('DD_Specialty', 'DEFINED_BY')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pending_specializations: list[DD_Specialty] = []

    def add_specialization(self, specialization: DD_Specialty):
        self._pending_specializations.append(specialization)

    def get_specializations(self):
        return self._pending_specializations

    @classmethod
    def get_or_create(cls, instance: "SpecialtyClassification") -> tuple["SpecialtyClassification", bool]:
        try:
            node = cls.nodes.get(name=instance.name)
            created = False
        except DoesNotExist:
            node = cls(name=instance.name).save()
            created = True

        node._pending_groups = instance.get_specializations()
        return node, created