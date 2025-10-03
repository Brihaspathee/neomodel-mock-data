from neomodel import StructuredNode, StringProperty
from neomodel.exceptions import DoesNotExist


class DD_Specialty(StructuredNode):
    value: str = StringProperty(required=True)
    taxonomyCode: str = StringProperty(unique_index=True, required=True)
    definition: str = StringProperty(required=True)
    group: str = StringProperty(required=True)
    classification: str = StringProperty(required=True)
    specialization: str = StringProperty(required=True)

    @classmethod
    def get_or_create(cls, instance: "DD_Specialty") -> tuple["DD_Specialty", bool]:
        try:
            node = cls.nodes.get(taxonomyCode=instance.taxonomyCode)
            created = False
        except DoesNotExist:
            node = cls(value=instance.value,
                       taxonomyCode=instance.taxonomyCode,
                       definition=instance.definition,
                       group=instance.group,
                       classification=instance.classification,
                       specialization=instance.specialization).save()
            created = True

        return node, created