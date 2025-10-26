from sqlalchemy import ForeignKey, Column, String, Integer, Date
from sqlalchemy.orm import relationship

from models.portico import Base


class PPPracCredCycle(Base):
    __tablename__ = "pp_prac_cred_cycle"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    prac_id = Column(Integer, ForeignKey("portown.pp_prac.id"))
    cred_type = Column(String, default=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    committee_date = Column(Date, nullable=True)
    is_delegated_cred = Column(String, default=False)
    affiliated_agency = Column(String, default=False)

    practitioner = relationship("PPPrac", back_populates="cred_cycles")

    def __repr__(self):
        return (f"<PPPracCredCycle(id={self.id}, "
                f"prac_id={self.prac_id}, "
                f"cred_type={self.cred_type}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"committee_date={self.committee_date}, "
                f"is_delegated_cred={self.is_delegated_cred}, "
                f"affiliated_agency={self.affiliated_agency})>")