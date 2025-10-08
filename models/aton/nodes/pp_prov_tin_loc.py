from neomodel import RelationshipTo, IntegerProperty

from models.aton.nodes.base_node import BaseNode


class PP_PROV_TIN_LOC(BaseNode):
    loc_id = IntegerProperty(required=True, unique_index=True, db_property='id')

    location = RelationshipTo("models.aton.nodes.location.Location", "SOURCES")