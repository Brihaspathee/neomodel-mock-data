from typing import Type

from neo4j.time import DateType
from neomodel import StringProperty, DateProperty, StructuredNode, RelationshipFrom
from neomodel.exceptions import DoesNotExist, MultipleNodesReturned

from models.aton.nodes.base_node import BaseNode


class Identifier(BaseNode):

    value: str= StringProperty(required=True)
    start_date: DateType= DateProperty(required=False)
    end_date: DateType= DateProperty(required=False)
    # @property
    # def uid(self):
    #     if hasattr(self, '_node') and self._node is not None:
    #         return self._node.element_id
    #     raise ValueError("Node is not yet saved; elementId is unavailable")

class NPI(Identifier):
    _node_labels = ('Identifier', 'NPI')

    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
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

    @classmethod
    def get_or_create(cls: Type["TIN"], lookup_props: dict, other_props: dict) -> tuple["TIN", bool]:
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

class MedicareID(Identifier):
    _node_labels = ('Identifier', 'MedicareID')
    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_MEDICARE_ID"
    )
    pass

class MedicaidID(Identifier):
    _node_labels = ('Identifier', 'MedicaidID')
    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_MEDICAID_ID"
    )
    state: str= StringProperty(required=False)
class LegacySystemID(Identifier):
    _node_labels = ('Identifier', 'LegacySystemID')

    system: str= StringProperty(required=False)
    systemIdType: str= StringProperty(required=False)

    organization = RelationshipFrom("models.aton.nodes.organization.Organization","HAS_LEGACY_SYSTEM_ID")
    network = RelationshipFrom("models.aton.nodes.network.Network","HAS_LEGACY_SYSTEM_ID")
    product = RelationshipFrom("models.aton.nodes.product.Product","HAS_LEGACY_SYSTEM_ID")
    location = RelationshipFrom("models.aton.nodes.location.Location","HAS_LEGACY_SYSTEM_ID")
    practitioner = RelationshipFrom("models.aton.nodes.practitioner.Practitioner","HAS_LEGACY_SYSTEM_ID")


class PPGID(Identifier):
    _node_labels = ('Identifier', 'PPGID'),

    # reverse link to org
    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_PPG_ID"
    )

    def __init__(self, *args, capitated_ppg=None, pcp_required=None, parent_ppg_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Temporary storage for other values associated with this identifier
        self.capitated_ppg = capitated_ppg
        self.pcp_required = pcp_required
        self.parent_ppg_id = parent_ppg_id