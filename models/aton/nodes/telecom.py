from neomodel import RelationshipFrom, StringProperty, StructuredNode

from models.aton.nodes.mock_data_test import MockDataTest


class Telecom(MockDataTest):

    phone: str = StringProperty(required=False)
    fax: str = StringProperty(required=False)
    tty: str = StringProperty(required=False)
    afterHoursNumber: str = StringProperty(required=False)
    email: str = StringProperty(required=False)
    secureEmail: str = StringProperty(required=False)
    website: str = StringProperty(required=False)

    contact = RelationshipFrom("models.aton.nodes.contact.Contact",
                               "TELECOM_IS")