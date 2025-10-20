from datetime import date

from neomodel import db, DateProperty
import logging

log = logging.getLogger(__name__)


def update_relationship_dates(rel, start_date=None, end_date=None):
    query = """
    MATCH ()-[r]->()
    WHERE elementId(r) = $element_id
    SET r.startDate = CASE WHEN $start_date IS NOT NULL THEN date($start_date) ELSE r.startDate END,
        r.endDate = CASE WHEN $end_date IS NOT NULL THEN date($end_date) ELSE r.endDate END
    RETURN r
    """
    db.cypher_query(
        query,
        {
            "element_id": rel.element_id,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
        },
    )

def convert_dates_to_native(node):
    log.debug(f"Type of the node: {type(node)}")
    log.debug(f"Node properties: {node.__class__.__dict__}")
    # Loop through all attributes of the class
    for attr_name, attr_obj in node.__class__.__dict__.items():
        # log.info(f"Attr Name:{attr_name}")
        # log.info(f"Attr Obj: {attr_obj}")
        # Only process DateProperty fields
        if isinstance(attr_obj, DateProperty):
            val = getattr(node, attr_name)
            if val and isinstance(val, date):
                # Determine the property name in Neo4j
                prop_name = getattr(attr_obj, 'db_property', None) or attr_name
                # Cypher query: match node by elementId and set native DATE
                query = f"""
                MATCH (n:{node.__class__.__name__})
                WHERE elementId(n) = elementId(n)
                SET n.{prop_name} = date($date_val)
                """
                db.cypher_query(query, {'date_val': val.isoformat()})