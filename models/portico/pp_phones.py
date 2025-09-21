from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.portico.base import Base

class PPPhones(Base):

    __tablename__ = "pp_phones"
    __table_args__ = {'schema': 'portown'}

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    areacode = Column(String, nullable=False)
    exchange = Column(String, nullable=False)
    num = Column(String, nullable=False)

    addresses = relationship('PPAddrPhones', back_populates='phone')

    def __repr__(self):
        """
        Provides a string representation of the `PPPhones` object for debugging and
        logging purposes. The returned string contains details about the `id`,
        `type`, `area_code`, `exchange`, and `number` attributes of the object.

        :return: A string representation of the `PPPhones` object
        :rtype: str
        """
        return (f"<PPPhones(id={self.id}, "
                f"type={self.type}, "
                f"areacode={self.areacode}, "
                f"exchange={self.exchange}, "
                f"number={self.num})>")