from neomodel import StringProperty, RelationshipFrom

from models.aton.nodes.base_node import BaseNode


class Disorder(BaseNode):
    disorder_type: str = StringProperty(required=True, db_property='type')

    prac_role = RelationshipFrom("models.aton.nodes.role_instance.RoleInstance",
                                    "TREATS_DISORDER")