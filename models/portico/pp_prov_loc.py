from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, Column, Integer, Boolean
from sqlalchemy.orm import relationship, Mapped
from models.portico.base import Base

if TYPE_CHECKING:
    from models.portico.pp_prov_loc_attrib import PPProvLocAttrib

class PPProvLoc(Base):

    __tablename__ = "pp_prov_loc"
    __table_args__ = {"schema": "portown"}

    prov_id = Column(Integer, ForeignKey("portown.pp_prov.id"), primary_key=True)
    loc_id = Column(Integer, ForeignKey("portown.pp_prov_tin_loc.id"), primary_key=True)
    PRIMARY = Column(Boolean, default=False)

    provider = relationship("PPProv", back_populates="prov_locs")
    location = relationship("PPProvTinLoc", back_populates="prov_locs")

    def __repr__(self):
        return (
            f"<PPProvLoc(prov_id={self.prov_id}, loc_id={self.loc_id}, primary={self.PRIMARY})>"
        )