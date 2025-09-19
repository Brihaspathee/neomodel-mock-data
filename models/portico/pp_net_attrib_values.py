from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from models.portico.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.portico.fmg_attribute_fields import FmgAttributeField


class PPNetAttribValues(Base):
    __tablename__ = "pp_net_attrib_values"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    net_attribute_id = Column(Integer, ForeignKey("portown.pp_net_attrib.id"))
    field_id = Column(Integer, ForeignKey("portown.fmg_attribute_fields.id"))
    value = Column(String, nullable=True)
    value_date = Column(Date, nullable=True)
    value_number = Column(Numeric, nullable=True)

    field: Mapped["FmgAttributeField"]= relationship("FmgAttributeField")

    def __repr__(self):
        return f"<PPNetAttribValues(id={self.id}, net_attribute_id={self.net_attribute_id}, field_id={self.field_id})>"