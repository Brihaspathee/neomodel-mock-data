from typing import Any

from neomodel import StructuredNode, StringProperty, RelationshipTo
from neomodel.exceptions import DoesNotExist

from models.aton.nodes.data_dictionary.dd_specialty_type import DD_SpecialtyType


class SpecialtyType(StructuredNode):

    definition: str = StringProperty(required=True)

    specialization = RelationshipTo('models.aton.nodes.data_dictionary.dd_specialty_type.DD_SpecialtyType', 'DEFINED_BY')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context: Any = None


    @classmethod
    def get_or_create(cls, instance: "SpecialtyType") -> tuple["SpecialtyType", bool]:
        try:
            node = cls.nodes.get(definition=instance.definition)
            created = False
        except DoesNotExist:
            node = cls(definition=instance.definition).save()
            created = True

        node.context = instance.context
        return node, created