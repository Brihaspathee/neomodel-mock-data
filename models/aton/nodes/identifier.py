from neo4j.time import DateType
from neomodel import StringProperty, DateProperty, StructuredNode, RelationshipFrom

from models.aton.nodes.mock_data_test import MockDataTest


class Identifier(MockDataTest):

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