from neomodel import StringProperty, BooleanProperty, RelationshipFrom

from models.aton.nodes.base_node import BaseNode


class Credentialing(BaseNode):
    cred_type: str = StringProperty(required=True, db_property='credType')
    geography_description: str = StringProperty(required=False, db_property='geographyDescription')
    fips: str = StringProperty(required=False, db_property='FIPS')
    cred_delegated: bool = BooleanProperty(required=False, db_property='credDelegeted')
    cred_organization: str = StringProperty(required=False, db_property='credentialingOrganization')

    practitioner = RelationshipFrom("models.aton.nodes.practitioner.Practitioner",
                                    "HAS_CREDENTIALING")
