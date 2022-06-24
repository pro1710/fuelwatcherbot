from sqlalchemy import (
    Table, 
    Column, 
    ForeignKey, 
    Integer, String,
    Float, 
    DateTime, 
    create_engine
)
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class FuelStation(Base):
    __tablename__ = 'fuel_station'

    id = Column(Integer, primary_key=True)
    internal_id = Column(Integer)
    link = Column(String(128))
    city = Column(String(64))
    address = Column(String(256))
    latitude = Column(Float(64))
    longitude = Column(Float(64))

    state = relationship("FuelStationState")
    storage = relationship("FuelStorage")
    
class FuelStationState(Base):
    __tablename__ = 'fuel_station_state'

    id = Column(Integer, primary_key=True)
    station_id = Column(Integer, ForeignKey('fuel_station.id'))
    state = Column(String(128))
    last_updated = Column(DateTime(), onupdate=datetime.datetime.now)

class FuelStorage(Base):
    __tablename__ = 'fuel_storage'

    id = Column(Integer, primary_key=True)
    station_id = Column(Integer, ForeignKey('fuel_station.id'))

    type = Column(String(16))
    status = Column(String(256), default='NA')

    last_updated = Column(DateTime(), onupdate=datetime.datetime.now)


def init_db():
    engine = create_engine("sqlite:///mydatabase.db")
    Base.metadata.create_all(engine)
    return engine

def open_db():
    pass