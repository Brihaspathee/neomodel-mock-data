from typing import Type, TypeVar

from neo4j.time import DateType
from neomodel import StringProperty, DateProperty, StructuredNode, RelationshipFrom
from neomodel.exceptions import DoesNotExist, MultipleNodesReturned

from models.aton.nodes.base_node import BaseNode

T = TypeVar("T", bound="Identifier")
class Identifier(BaseNode):

    value: str= StringProperty(required=True)
    start_date: DateType= DateProperty(required=False, db_property='startDate')
    end_date: DateType= DateProperty(required=False, db_property='endDate')

    @classmethod
    def get_or_create(cls: Type[T], lookup_props: dict, other_props: dict) -> tuple[
        T, bool]:
        try:
            node = cls.nodes.get(**lookup_props)
            created = False
        except DoesNotExist:
            node = cls(**lookup_props, **other_props).save()
            created = True
        except MultipleNodesReturned as e:
            raise MultipleNodesReturned(
                f"Multiple nodes returned for {cls.__name__} with lookup props {lookup_props}"
            ) from e
        return node, created

class NPI(Identifier):
    _node_labels = ('Identifier', 'NPI')

    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_NPI"
    )
    practitioner = RelationshipFrom(
        "models.aton.nodes.practitioner.Practitioner",
        "HAS_NPI"
    )

class TIN(Identifier):
    _node_labels = ('Identifier', 'TIN' )
    legal_name: str= StringProperty(required=False)
    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_TIN"
    )
    def __repr__(self):
        return f"{self.value} - {self.legal_name}"

class MedicareID(Identifier):
    _node_labels = ('Identifier', 'MedicareID')
    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_MEDICARE_ID"
    )
    practitioner = RelationshipFrom(
        "models.aton.nodes.practitioner.Practitioner",
        "HAS_MEDICARE_ID"
    )

class MedicaidID(Identifier):
    _node_labels = ('Identifier', 'MedicaidID')
    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_MEDICAID_ID"
    )
    practitioner = RelationshipFrom(
        "models.aton.nodes.practitioner.Practitioner",
        "HAS_MEDICAID_ID"
    )
    state: str= StringProperty(required=False)

class LegacySystemID(Identifier):
    _node_labels = ('Identifier', 'LegacySystemID')

    system: str= StringProperty(required=False)
    systemIdType: str= StringProperty(required=False)
    description: str= StringProperty(required=False)

    organization = RelationshipFrom("models.aton.nodes.organization.Organization","HAS_LEGACY_SYSTEM_ID")
    network = RelationshipFrom("models.aton.nodes.network.Network","HAS_LEGACY_SYSTEM_ID")
    product = RelationshipFrom("models.aton.nodes.product.Product","HAS_LEGACY_SYSTEM_ID")
    location = RelationshipFrom("models.aton.nodes.location.Location","HAS_LEGACY_SYSTEM_ID")
    practitioner = RelationshipFrom("models.aton.nodes.practitioner.Practitioner","HAS_LEGACY_SYSTEM_ID")

class DEA_Number(Identifier):
    _node_labels = ('Identifier', 'DEA_Number')
    practitioner = RelationshipFrom(
        "models.aton.nodes.practitioner.Practitioner",
        "HAS_DEA_NUMBER"
    )
    state: str= StringProperty(required=False)

class PPGID(Identifier):
    _node_labels = ('Identifier', 'PPGID'),

    # reverse link to org
    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_PPG_ID"
    )