from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from models.portico.base import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.portico.pp_prov_loc_attrib_values import PPProvLocAttribValues
    from models.portico.pp_prov import PPProv
    from models.portico.pp_prov_tin_loc import PPProvTinLoc
    from models.portico.fmg_attribute_types import FmgAttributeType


class PPProvLocAttrib(Base):
    """
    Represents the attributes associated with a provider.

    This class maps the relationship between providers and their attributes. It links
    a provider (referenced by `prov_id`) to specific attribute types (referenced by
    `attribute_id`). Each attribute is uniquely identified by its `id`. The class also
    establishes relationships to the provider, attribute type, and the values associated
    with a provider's attributes.

    :ivar id: Unique identifier for the provider attribute entry in the database.
    :type id: int
    :ivar prov_id: Identifier for the associated provider.
    :type prov_id: int
    :ivar attribute_id: Identifier for the corresponding attribute type.
    :type attribute_id: int
    :ivar provider: Relationship providing access to the provider associated with this attribute.
    :type provider: PPProv
    :ivar values: Relationship providing access to the values linked to this provider attribute.
    :type values: list[PPProvAttribValues]
    :ivar attribute_type: Relationship providing access to the corresponding attribute type details.
    :type attribute_type: FmgAttributeType
    """
    __tablename__ = "pp_prov_loc_attrib"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    prov_id = Column(Integer, ForeignKey("portown.pp_prov.id"))
    loc_id = Column(Integer, ForeignKey("portown.pp_prov_tin_loc.id"))
    attribute_id = Column(Integer, ForeignKey("portown.fmg_attribute_types.id"))

    # Relationships
    provider: Mapped["PPProv"] = relationship("PPProv", back_populates="loc_attributes")
    location: Mapped["PPProvTinLoc"] = relationship("PPProvTinLoc")  # one-way
    attribute_type = relationship("FmgAttributeType")
    values: Mapped[List["PPProvLocAttribValues"]] = relationship("PPProvLocAttribValues")

    def __repr__(self):
        """
        Provides a string representation of the object for debugging and logging purposes. The returned
        string includes key attributes of the instance to help identify its state and key properties.

        :return: A string containing a concise representation of the object, displaying its ID,
            provider ID, and attribute ID.
        :rtype: str
        """
        return (f"<PPProvAttrib(id={self.id}, "
                f"prov_id={self.prov_id}, "
                f"attribute_id={self.attribute_id})>")