from neo4j.time import DateType
from neomodel import StringProperty, DateProperty, StructuredNode


class Identifier(StructuredNode):

    value: str= StringProperty(required=True)
    startDate: DateType= DateProperty(required=False)
    endDate: DateType= DateProperty(required=False)
    # @property
    # def uid(self):
    #     if hasattr(self, '_node') and self._node is not None:
    #         return self._node.element_id
    #     raise ValueError("Node is not yet saved; elementId is unavailable")

class NPI(Identifier):
    _node_labels = ('Identifier', 'NPI')

class TIN(Identifier):
    _node_labels = ('Identifier', 'TIN' )
    legal_name: str= StringProperty(required=False)
    def __repr__(self):
        return f"{self.value} - {self.legal_name}"

class MedicareId(Identifier):
    _node_labels = ('Identifier', 'MedicareID')
    pass

class MedicaidId(Identifier):
    _node_labels = ('Identifier', 'MedicaidID')
    state: str= StringProperty(required=False)

class PPGID(Identifier):
    _node_labels = ('Identifier', 'PPGID')