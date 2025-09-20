from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from models.portico.base import Base

class PPAddr(Base):
    __tablename__ = 'pp_addr'
    __table_args__ = {'schema': 'portown'}

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    addr1 = Column(String, nullable=False)
    addr2 = Column(String, nullable=True)
    # city = Column(String, nullable=False)
    zip = Column(String, nullable=False)
    # county = Column(String, nullable=True)
    county_fips = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    # City and county Foreign Keys
    city_id = Column(Integer, ForeignKey('portown.fmg_cities.id'))
    county_id = Column(Integer, ForeignKey('portown.fmg_counties.id'))

    # providers = relationship("PPProv", back_populates="address")
    phones = relationship("PPAddrPhones", back_populates="address")
    provider_address = relationship("PPProvAddr", back_populates="address")

    city = relationship("FmgCities")
    county = relationship("FmgCounties")

    def __repr__(self):
        """
        Provides a string representation of the PPAddr object. The returned string
        includes all the attributes of the PPAddr instance in a clear and
        human-readable format, making it useful for debugging and logging purposes.

        :return: A string representing the PPAddr object with its attributes.
        :rtype: str
        """
        return (f"<PPAddr(id={self.id}, "
                f"type={self.type}, "
                f"addr1={self.addr1}, "
                f"addr2={self.addr2}, "
                # f"city={self.city}, "
                f"zip={self.zip}, "
                # f"county={self.county}, "
                f"fips={self.county_fips}, "
                f"latitude={self.latitude}, "
                f"longitude={self.longitude}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date})>")
