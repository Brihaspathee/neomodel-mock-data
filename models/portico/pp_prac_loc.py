from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from models.portico import Base


class PPPracLoc(Base):
    __tablename__ = "pp_prac_loc"
    __table_args__ = {"schema": "portown"}

    prov_id = Column(Integer, ForeignKey("portown.pp_prov.id"), primary_key=True)
    prac_id = Column(Integer, ForeignKey("portown.pp_prac.id"), primary_key=True)
    loc_id = Column(Integer, ForeignKey("portown.pp_prov_tin_loc.id"), primary_key=True)
    PRIMARY = Column(String, default=False)

    provider = relationship("PPProv", back_populates="prac_locs")
    practitioner = relationship("PPPrac", back_populates="locations")
    location = relationship("PPProvTinLoc")

    def __repr__(self):
        return (
            f"<PPPracLoc(prov_id={self.prov_id}, prac_id={self.prac_id}, loc_id={self.loc_id}, PRIMARY={self.PRIMARY})>"
        )