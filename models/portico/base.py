from sqlalchemy.orm import declarative_base, DeclarativeBase

"""
This module contains the Base class, which is used to define the declarative base for all models in the Portico database.
"""
Base: type[DeclarativeBase] = declarative_base()