from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from models.portico.base import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.portico.pp_prac_loc_attrib_values import PPPracLocAttribValues
    from models.portico.pp_prac import PPPrac
    from models.portico.pp_prov_tin_loc import PPProvTinLoc
    from models.portico.fmg_attribute_types import FmgAttributeType


class PPPracLocAttrib(Base):

    __tablename__ = "pp_prac_loc_attrib"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    prov_id = Column(Integer, ForeignKey("portown.pp_prov.id"))
    prac_id = Column(Integer, ForeignKey("portown.pp_prac.id"))
    loc_id = Column(Integer, ForeignKey("portown.pp_prov_tin_loc.id"))
    attribute_id = Column(Integer, ForeignKey("portown.fmg_attrib_types.id"))

    # Relationships
    practitioner: Mapped["PPPrac"] = relationship("PPPrac", back_populates="loc_attributes")
    location: Mapped["PPProvTinLoc"] = relationship("PPProvTinLoc")  # one-way
    attribute_type = relationship("FmgAttributeType")
    values: Mapped[List["PPPracLocAttribValues"]] = relationship("PPPracLocAttribValues")

    def __repr__(self):

        return (f"<PPPracLocAttrib(id={self.id}, "
                f"prov_id={self.prov_id}, "
                f"prac_id={self.prac_id}, "
                f"loc_id={self.loc_id}, "
                f"attribute_id={self.attribute_id})>")