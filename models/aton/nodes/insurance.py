from neomodel import StringProperty, BooleanProperty, DateProperty, RelationshipFrom

from models.aton.nodes.base_node import BaseNode
import logging

from models.aton.nodes.node_utils import convert_dates_to_native

log = logging.getLogger(__name__)


class Insurance(BaseNode):
    carrier: str = StringProperty(required=True, db_property='carrier')
    value: str = StringProperty(required=False, db_property='value')
    coverage_amount: str = StringProperty(required=False, db_property='coverageAmount')
    coverage_type: str = StringProperty(required=False, db_property='coverageType')
    unlimited_coverage: bool = BooleanProperty(required=False, db_property='unlimitedCoverage')
    start_date: str = DateProperty(required=False, db_property='startDate')
    end_date: str = DateProperty(required=False, db_property='endDate')

    practitioner = RelationshipFrom("models.aton.nodes.practitioner.Practitioner",
                                    "HAS_INSURANCE")

    def save(self, *args, **kwargs):
        node = super().save(*args, **kwargs)
        log.debug(f"Node saved: {node}")
        convert_dates_to_native(node)
        return node
