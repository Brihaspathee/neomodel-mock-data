from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.portico.base import Base

class PPProvTIN(Base):
    """
    Represents the PPProvTIN database table.

    This class defines the schema for the `pp_prov_tin` table in the `portown` schema.
    It contains columns for storing the primary key `id`, `name`, and `tin` attributes.
    The class also establishes a relationship to the `PPProv` class to manage associated data.
    This class is typically used to interact with provider TIN (Taxpayer Identification Number)
    information in the database.

    :ivar id: The primary key of the table.
    :type id: Integer
    :ivar name: The name associated with the provider TIN.
    :type name: String
    :ivar tin: The Taxpayer Identification Number of the provider.
    :type tin: Integer
    :ivar providers: A relationship linking to the `PPProv` class, representing providers
                     associated with this TIN.
    :type providers: relationship
    """
    __tablename__ = "pp_prov_tin"
    __table_args__ = {'schema': 'portown'}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tin = Column(Integer, nullable=False)

    providers = relationship("PPProv", back_populates="tin")

    def __repr__(self):
        """
        Provides a string representation of the `PPProvTIN` object including its key attributes.

        The string representation includes the `id`, `name`, and `tin` properties of the
        object, facilitating a structured and human-readable output which can be useful
        for debugging and logging purposes.

        :return: A formatted string representing the `PPProvTIN` object with its key attributes.
        :rtype: str
        """
        return (f"<PPProvTIN(id={self.id}, "
                f"name={self.name}, "
                f"tin={self.tin})>")