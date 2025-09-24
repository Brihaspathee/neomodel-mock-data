from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from models.portico import Base


class PPPracNetCycle(Base):
    __tablename__ = "pp_prac_net_cycle"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    prac_id = Column(Integer, ForeignKey("portown.pp_prac.id"))
    net_id = Column(Integer, ForeignKey("portown.pp_net.id"))
    status = Column(String, nullable=True)

    # Relationships
    loc_cycles = relationship("PPPracNetLocCycle", back_populates="prac_net_cycle")
    practitioner = relationship("PPPrac", back_populates="networks")
    network = relationship("PPNet")