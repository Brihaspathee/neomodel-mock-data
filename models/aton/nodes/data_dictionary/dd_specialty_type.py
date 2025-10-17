from typing import Any

from neomodel import StructuredNode, StringProperty, RelationshipFrom, RelationshipTo
from neomodel.exceptions import DoesNotExist

from models.aton.nodes.identifier import LegacySystemIdentifier


class DD_SpecialtyType(StructuredNode):
    value: str = StringProperty(required=True)
    code: str = StringProperty(unique_index=True, required=True)
    description: str = StringProperty(required=True)
    group: str = StringProperty(required=True)
    classification: str = StringProperty(required=True)

    specialty = RelationshipFrom('models.aton.nodes.data_dictionary.specialty_type.SpecialtyType', 'DEFINED_BY')
    legacySystemIdentifier = RelationshipTo('models.aton.nodes.identifier.LegacySystemIdentifier', 'HAS_LEGACY_SYSTEM_IDENTIFIER')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context: Any = None

    @classmethod
    def get_or_create(cls, instance: "DD_SpecialtyType") -> tuple["DD_SpecialtyType", bool]:
        try:
            node = cls.nodes.get(code=instance.code)
            created = False
        except DoesNotExist:
            node = cls(value=instance.value,
                       code=instance.code,
                       description=instance.description,
                       group=instance.group,
                       classification=instance.classification).save()
            created = True
        node.context = instance.context
        return node, created