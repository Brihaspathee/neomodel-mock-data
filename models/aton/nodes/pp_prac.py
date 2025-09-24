from neomodel import StringProperty, RelationshipTo

from models.aton.nodes.mock_data_test import MockDataTest


class PP_PRAC(MockDataTest):

    prac_id = StringProperty(required=True)

    aton_prac = RelationshipTo("models.aton.nodes.practitioner.Practitioner", "SOURCES")