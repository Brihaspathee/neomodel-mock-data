from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.portico.base import Base

class PPSpec(Base):
    """
    Represents the specification of a specific category in a system.

    This class is tied to the database schema `portown` and corresponds to
    the `pp_spec` table. It is designed to store and manage data related
    to a specific specification type, its description, and whether a site
    visit is required. The class also establishes a relationship with the
    providers (`PPProv`) that are associated with this specification.

    :ivar id: The unique identifier for the specification.
    :type id: int
    :ivar type: The type of specification. This field is required.
    :type type: str
    :ivar description: An optional description providing additional
        information about the specification.
    :type description: str or None
    :ivar site_visit_req: An optional flag indicating whether a site visit
        is required for this specification.
    :type site_visit_req: str or None
    :ivar providers: A collection of providers (`PPProv`) associated with
        this specification. This establishes a relationship with the
        `PPProv` class, where the `specialty` attribute is used for
        back-population.
    :type providers: list of PPProv
    """
    __tablename__ = "pp_spec"
    __table_args__ = {'schema': 'portown'}

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    description = Column(String, nullable=True)
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
                f"description={self.description}, "
                f"site_visit_req={self.site_visit_req})>")