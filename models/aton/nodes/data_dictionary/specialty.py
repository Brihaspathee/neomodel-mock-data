from typing import Any

from neomodel import StructuredNode, StringProperty, RelationshipTo
from neomodel.exceptions import DoesNotExist

from models.aton.nodes.specialty_group import SpecialtyGroup


class Specialty(StructuredNode):

    definition: str = StringProperty(required=True)

    groups = RelationshipTo('SpecialtyGroup', 'GROUPED_BY')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pending_groups: list[SpecialtyGroup] = []

    def add_group(self, group: SpecialtyGroup):
        self._pending_groups.append(group)

    def get_groups(self):
        return self._pending_groups


    @classmethod
    def get_or_create(cls, instance: "Specialty") -> tuple["Specialty", bool]:
        try:
            node = cls.nodes.get(definition=instance.definition)
            created = False
        except DoesNotExist:
            node = cls(definition=instance.definition).save()
            created = True

        node._pending_groups = instance.get_groups()
        return node, created