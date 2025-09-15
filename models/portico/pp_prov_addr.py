from sqlalchemy import ForeignKey, Column, String, Integer
from sqlalchemy.orm import relationship, Mapped
from models.portico.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.portico.pp_addr import PPAddr

class PPProvAddr(Base):
    """
    Represents the association between providers and addresses.

    This class maps the relationship between a provider and its associated
    address in the database. It is part of the `portown` schema and uses the
    SQLAlchemy ORM for database interactions. Each instance of this class links
    a provider to an address and defines the relationships between the data
    models for provider and address entities.

    :ivar id: Unique identifier for the provider-address association.
    :type id: int
    :ivar prov_id: Identifier linking to the associated provider.
    :type prov_id: int
    :ivar address_id: Identifier linking to the associated address.
    :type address_id: int
    :ivar providers: Relationship to the `PPProv` model.
    :type providers: sqlalchemy.orm.RelationshipProperty
    :ivar address: Relationship to the `PPAddr` model.
    :type address: sqlalchemy.orm.RelationshipProperty
    """
    __tablename__ = "pp_prov_addr"
    __table_args__ = {"schema": "portown"}

    # id = Column(Integer, primary_key=True)
    prov_id = Column(Integer, ForeignKey("portown.pp_prov.id"), primary_key=True)
    address_id = Column(Integer, ForeignKey("portown.pp_addr.id"), primary_key=True)

    providers = relationship("PPProv", back_populates="addresses")
    address: Mapped["PPAddr"] = relationship("PPAddr", back_populates="provider_address")

    def __repr__(self):
        """
        Provides a string representation of the PPProvAddr object, including its
        id, prov_id, and address_id attributes. This is primarily useful for
        debugging purposes or logging, allowing identification of the object's
        state easily in string form.

        :return: A string representation of the PPProvAddr object.
        :rtype: str
        """
        return (f"<PPProvAddr( "
                f"prov_id={self.prov_id}, "
                f"address_id={self.address_id})>")