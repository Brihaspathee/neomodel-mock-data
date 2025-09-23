from neomodel import StringProperty, RelationshipTo, StructuredNode

from models.aton.nodes.mock_data_test import MockDataTest


class PP_PROV_TIN_LOC(MockDataTest):
    # __label__ = "PP_Prov_TIN_Loc"
    loc_id = StringProperty(required=True)

    aton_location = RelationshipTo("models.aton.nodes.location.Location", "SOURCES")