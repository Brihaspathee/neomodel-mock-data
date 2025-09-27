from neomodel import StructuredNode, StringProperty
from neomodel.exceptions import DoesNotExist


class DD_Specialty(StructuredNode):
    name: str = StringProperty(required=True)
    taxonomy: str = StringProperty(unique_index=True, required=True)
    definition: str = StringProperty(required=True)

    @classmethod
    def get_or_create(cls, instance: "DD_Specialty") -> tuple["DD_Specialty", bool]:
        try:
            node = cls.nodes.get(taxonomy=instance.taxonomy)
            created = False
        except DoesNotExist:
            node = cls(name=instance.name,
                       taxonomy=instance.taxonomy,
                       definition=instance.definition).save()
            created = True

        return node, created