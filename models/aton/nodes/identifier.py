from typing import Type, TypeVar

from neomodel import StringProperty, DateProperty, StructuredNode, RelationshipFrom
from neomodel.exceptions import DoesNotExist, MultipleNodesReturned

from models.aton.nodes.base_node import BaseNode
from models.aton.nodes.node_utils import convert_dates_to_native
import logging

log = logging.getLogger(__name__)

T = TypeVar("T", bound="Identifier")
class Identifier(BaseNode):

    value: str= StringProperty(required=True)

    @classmethod
    def get_or_create(cls: Type[T], lookup_props: dict, other_props: dict) -> tuple[
        T, bool]:
        try:
            node = cls.nodes.get(**lookup_props)
            created = False
        except DoesNotExist:
            log.info(">>> Creating an identifier node with lookup props %s", lookup_props)
            log.info(">>> Creating an identifier node with other props %s", other_props)
            node = cls(**lookup_props, **other_props).save()
            # node = cls(**lookup_props)
            # for k, v in other_props.items():
            #     setattr(node, k, v)
            # log.info(">>> Sav identifier node %s", node)
            # node.save()
            created = True
        except MultipleNodesReturned as e:
            raise MultipleNodesReturned(
                f"Multiple nodes returned for {cls.__name__} with lookup props {lookup_props}"
            ) from e
        return node, created

    def save(self, *args, **kwargs):
        log.debug(">>> Saving an identifier node")
        node = super().save(*args, **kwargs)
        convert_dates_to_native(self)
        return node

class NPI(Identifier):
    _node_labels = ('Identifier', 'NPI')

    start_date: DateProperty = DateProperty(required=False, db_property='startDate')
    end_date: DateProperty = DateProperty(required=False, db_property='endDate')

    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_NPI"
    )
    practitioner = RelationshipFrom(
        "models.aton.nodes.practitioner.Practitioner",
        "HAS_NPI"
    )

class TIN(Identifier):
    _node_labels = ('Identifier', 'TIN' )
    legal_name: str= StringProperty(required=False, db_property='legalName')
    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_TIN"
    )
    def __repr__(self):
        return f"{self.value} - {self.legal_name}"

class MedicareID(Identifier):
    _node_labels = ('Identifier', 'MedicareID')
    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_MEDICARE_ID"
    )
    practitioner = RelationshipFrom(
        "models.aton.nodes.practitioner.Practitioner",
        "HAS_MEDICARE_ID"
    )

class MedicaidID(Identifier):
    _node_labels = ('Identifier', 'MedicaidID')
    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_MEDICAID_ID"
    )
    practitioner = RelationshipFrom(
        "models.aton.nodes.practitioner.Practitioner",
        "HAS_MEDICAID_ID"
    )
    start_date: DateProperty = DateProperty(required=False, db_property='startDate')
    end_date: DateProperty = DateProperty(required=False, db_property='endDate')
    state: str= StringProperty(required=False)

class LegacySystemIdentifier(Identifier):
    _node_labels = ('Identifier', 'LegacySystemIdentifier')

    system: str= StringProperty(required=False)
    systemIdType: str= StringProperty(required=False)
    description: str= StringProperty(required=False)

    organization = RelationshipFrom("models.aton.nodes.organization.Organization","HAS_LEGACY_SYSTEM_IDENTIFIER")
    network = RelationshipFrom("models.aton.nodes.network.Network","HAS_LEGACY_SYSTEM_IDENTIFIER")
    product = RelationshipFrom("models.aton.nodes.product.Product","HAS_LEGACY_SYSTEM_IDENTIFIER")
    location = RelationshipFrom("models.aton.nodes.location.Location","HAS_LEGACY_SYSTEM_IDENTIFIER")
    practitioner = RelationshipFrom("models.aton.nodes.practitioner.Practitioner","HAS_LEGACY_SYSTEM_IDENTIFIER")
    dd_specialty = RelationshipFrom('models.aton.nodes.data_dictionary.dd_specialty_type.DD_SpecialtyType', 'HAS_LEGACY_SYSTEM_IDENTIFIER')

class DEA_Number(Identifier):
    _node_labels = ('Identifier', 'DEA_Number')
    practitioner = RelationshipFrom(
        "models.aton.nodes.practitioner.Practitioner",
        "HAS_DEA_NUMBER"
    )
    state: str= StringProperty(required=False)
    start_date: DateProperty = DateProperty(required=False, db_property='startDate')
    end_date: DateProperty = DateProperty(required=False, db_property='endDate')

class PPGID(Identifier):
    _node_labels = ('Identifier', 'PPGID'),

    # reverse link to org
    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_PPG_ID"
    )

class ECP_ID(Identifier):
    _node_labels = ('Identifier', 'ECP_ID')
    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_ECP_ID"
    )

class Medicaid_Clinic_ID(Identifier):
    _node_labels = ('Identifier', 'Medicaid_Clinic_ID')
    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_MEDICAID_CLINIC_ID"
    )

