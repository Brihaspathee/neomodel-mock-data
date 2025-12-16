from neomodel import StructuredNode, StringProperty, FloatProperty, RelationshipFrom

from models.aton.nodes.base_node import BaseNode


class Address(BaseNode):
    streetAddress = StringProperty(required=True)
    secondaryAddress = StringProperty(required=False)
    city = StringProperty(required=False)
    state = StringProperty(required=False)
    zip_code = StringProperty(required=False, db_property="zipCode")
    county = StringProperty(required=False)
    county_fips = StringProperty(required=False, db_property="countyFIPS")
    latitude = StringProperty(required=False)
    longitude = StringProperty(required=False)

    contact = RelationshipFrom("models.aton.nodes.contact.Contact",
                               "ADDRESS_IS")