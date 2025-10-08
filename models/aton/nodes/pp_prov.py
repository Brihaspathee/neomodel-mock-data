from neomodel import StringProperty, RelationshipTo, IntegerProperty

from models.aton.nodes.base_node import BaseNode


class PP_PROV(BaseNode):
    prov_id = IntegerProperty(required=True, unique_index=True, db_property='id')

    organization = RelationshipTo("models.aton.nodes.organization.Organization", "SOURCES")