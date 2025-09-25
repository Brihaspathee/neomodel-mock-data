from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from models.portico import Base


class PPPrac(Base):
    __tablename__ = "pp_prac"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    fname = Column(String, nullable=False)
    mname = Column(String, nullable=True)
    lname = Column(String, nullable=False)
    xname = Column(String, nullable=False)
    degree = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    ssn = Column(String, nullable=False)
    email = Column(String, nullable=False)
    salutation = Column(String, nullable=False)

    # Relationships
    networks = relationship("PPPracNetCycle", back_populates="practitioner")
    locations = relationship("PPPracLoc", back_populates="practitioner")


    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return (f"<PPPrac(id={self.id}, "
                f"fname={self.fname}, "
                f"mname={self.mname}, "
                f"lname={self.lname}, >")