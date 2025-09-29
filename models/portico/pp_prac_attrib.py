from typing import List, TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from models.portico import Base

if TYPE_CHECKING:
    from models.portico.pp_prac_attrib_values import PPPracAttribValues

class PPPracAttrib(Base):
    __tablename__ = "pp_prac_attrib"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    prac_id = Column(Integer, ForeignKey("portown.pp_prac.id"))
    attribute_id = Column(Integer, ForeignKey("portown.fmg_attrib_types.id"))

    practitioner = relationship("PPPrac", back_populates="attributes")
    # values = relationship("PPProvAttribValues", back_populates="provider_attribute")
    values: Mapped[List["PPPracAttribValues"]] = relationship("PPPracAttribValues")
    # attribute_type = relationship("FmgAttributeType", back_populates="provider_attributes")
    attribute_type = relationship("FmgAttributeType")

    def __repr__(self):
        return (f"<PPPracAttrib(id={self.id}, "
                f"prac_id={self.prac_id}, "
                f"attribute_id={self.attribute_id})>")