from neomodel import db

from models.aton.nodes.organization import Organization
from models.aton.nodes.practitioner import Practitioner
from models.aton.nodes.role_instance import RoleInstance


def get_role_instance_for_prac_org(prac:Practitioner, org: Organization):
    query = """
        MATCH (p:Practitioner)-[:HAS_ROLE]->(r:RoleInstance)-[:CONTRACTED_BY]->(o:Organization)
        WHERE elementId(p) = $practitioner_id AND elementId(o) = $organization_id
        RETURN r
        """
    results, meta = db.cypher_query(query, {
        "practitioner_id": prac.element_id,
        "organization_id": org.element_id
    })
    return [RoleInstance.inflate(row[0]) for row in results]

def get_role_instances(prac:Practitioner, org: Organization):
    practitioner_roles = prac.role.all()
    org_roles = org.contracted_by.all()

    # return all roles that are both in the practitioner and the organization
    return [role for role in practitioner_roles if role in org_roles]

