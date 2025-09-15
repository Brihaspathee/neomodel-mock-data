from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped

from models.portico.base import Base
from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from models.portico.pp_prov_addr import PPProvAddr
    from models.portico.pp_prov_attrib import PPProvAttrib
    from models.portico.pp_prov_loc import PPProvLoc
    from models.portico.pp_prov_loc_attrib import PPProvLocAttrib
    from models.portico.pp_prov_tin_loc import PPProvTinLoc


class PPProv(Base):
    """
    Represents a provider entity within the `portown` schema.

    This class defines the basic structure, relationships, and attributes of a provider in the `pp_prov`
    table within the database schema `portown`. The `PPProv` class is designed to manage providers and
    their related data, including relationships to TIN (Taxpayer Identification Number), provider type,
    address, specialty, and other linked details.

    :ivar id: Primary key representing the unique identifier of the provider.
    :type id: int
    :ivar name: Name of the provider (non-nullable).
    :type name: str
    :ivar tin_id: Foreign key linking to the TIN details in `pp_prov_tin` table.
    :type tin_id: str | None
    :ivar prov_type_id: Foreign key linking to the provider type in `pp_prov_type` table.
    :type prov_type_id: str | None
    :ivar address_id: Foreign key linking to the address in `pp_addr` table.
    :type address_id: str | None
    :ivar spec_id: Foreign key linking to the specialty in `pp_spec` table.
    :type spec_id: str | None
    :ivar tin: Relationship to the `PPProvTIN` entity, enabling access to details about the TIN.
    :type tin: PPProvTIN
    :ivar prov_type: Relationship to the `PPProvType` entity, enabling access to the provider type details.
    :type prov_type: PPProvType
    :ivar address: Relationship to the `PPAddr` entity, providing information about the provider’s main address.
    :type address: PPAddr
    :ivar specialty: Relationship to the `PPSpec` entity, indicating the specialty of the provider.
    :type specialty: PPSpec
    :ivar addresses: Relationship to the `PPProvAddr` entity, enabling access to secondary or additional addresses.
    :type addresses: list[PPProvAddr]
    :ivar attributes: Relationship to the `PPProvAttrib` entity, allowing access to the provider’s additional attributes.
    :type attributes: list[PPProvAttrib]
    """
    __tablename__ = "pp_prov"
    __table_args__ = {'schema': 'portown'}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tin_id = Column(String, ForeignKey('portown.pp_prov_tin.id'))
    prov_type_id = Column(String, ForeignKey('portown.pp_prov_type.id'))
    address_id = Column(String, ForeignKey('portown.pp_addr.id'))
    spec_id = Column(String, ForeignKey('portown.pp_spec.id'))

    tin = relationship("PPProvTIN", back_populates="providers")
    # prov_type = relationship("PPProvType", back_populates="providers")
    prov_type = relationship("PPProvType")
    # address = relationship("PPAddr", back_populates="providers")
    address = relationship("PPAddr")
    # specialty = relationship("PPSpec", back_populates="providers")
    specialty = relationship("PPSpec")

    addresses: Mapped[List["PPProvAddr"]] = relationship("PPProvAddr", back_populates="providers")

    attributes: Mapped[List["PPProvAttrib"]] = relationship("PPProvAttrib", back_populates="provider")
    loc_attributes: Mapped[List["PPProvLocAttrib"]] = relationship(
        "PPProvLocAttrib",
        back_populates="provider",
        cascade="all, delete-orphan"
    )

    # Association table mapping
    prov_locs: Mapped[List["PPProvLoc"]] = relationship("PPProvLoc", back_populates="provider")

    # Many-to-many: provider -> locations via pp_prov_loc
    # locations: Mapped[List["PPProvTinLoc"]] = relationship(
    #     "PPProvTinLoc",
    #     secondary="portown.pp_prov_loc",
    #     viewonly = True,
    #     overlaps = "prov_locs,provider"
    # )

    networks = relationship("PPProvNetCycle",
                            back_populates="provider")

    def __repr__(self):

        """
        Provides a string representation of the PPProv object. This method
        is intended to return a concise representation of the primary
        identification details of a PPProv instance. The string is formatted
        to include the instance's id, name, tin_id, prov_type_id, address_id,
        and specialty_id in an easily readable manner.

        :return: A string that represents the instance's key attributes.
        :rtype: str
        """

        return (f"<PPProv(id={self.id}, name={self.name}"
                f"tin_id={self.tin_id}, "
                f"prov_type_id={self.prov_type_id}, "
                f"address_id={self.address_id}, "
                f"spec_id={self.spec_id})>")
