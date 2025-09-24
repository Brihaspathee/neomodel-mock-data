from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from models.portico import Base


class PPPracNetLocCycle(Base):
    __tablename__ = "pp_prac_net_loc_cycle"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    prac_id = Column(Integer, ForeignKey("portown.pp_prac.id"))
    prov_id = Column(Integer, ForeignKey("portown.pp_prov.id"))
    loc_id = Column(Integer, ForeignKey("portown.pp_prov_tin_loc.id"))
    prac_net_cycle_id = Column(Integer, ForeignKey("portown.pp_prac_net_cycle.id"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # Relationships
    provider = relationship("PPProv", back_populates="prac_net_loc_cycles")
    location = relationship("PPProvTinLoc")
    prac_net_cycle = relationship("PPPracNetCycle", back_populates="loc_cycles")