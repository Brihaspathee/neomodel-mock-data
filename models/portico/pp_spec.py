from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.portico.base import Base

class PPSpec(Base):
    __tablename__ = "pp_spec"
    __table_args__ = {'schema': 'portown'}

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    ds = Column(String, nullable=True)
    site_visit_req = Column(String, nullable=True)

    # providers = relationship("PPProv", back_populates="specialty")

    def __repr__(self):
        """
        Provides a string representation of the PPSpec object, which includes key
        attributes such as id, type, description, and whether a site visit is required.

        :return: A string representation of the `PPSpec` instance
        :rtype: str
        """
        return (f"<PPSpec(id={self.id}, type={self.type}, "
                f"description={self.ds}, "
                f"site_visit_req={self.site_visit_req})>")