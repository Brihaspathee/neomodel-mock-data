from neomodel import StringProperty, RelationshipTo, IntegerProperty

from models.aton.nodes.base_node import BaseNode


class PP_PRAC(BaseNode):
    prac_id = IntegerProperty(required=True, unique_index=True, db_property='id')

    practitioner = RelationshipTo("models.aton.nodes.practitioner.Practitioner", "SOURCES")