#!/usr/bin/python3
"""This is the place class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from models.review import Review
import models
from os import getenv

place_amenity = Table('place_amenity', Base.metadata,
                      Column("place_id", String(60), ForeignKey("places.id"),
                             primary_key=True, nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"), primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    # for DBStorage
    reviews = relationship("Review", cascade="all, delete-orphan",
                           backref="place")
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        # For FileStorage
        @property
        def reviews(self):
            """Returns the list of Review instances with place_id equal to the
            current Place.id"""
            ls = []
            for value in storage.all("Review").values():
                if value.place_id == self.id:
                    ls.append(value)
            return ls

        @property
        def amenities(self):
            """Returns the list of Amenity instances based on the attribute
            amenity_ids that contains all Amenity.id linked to the Place"""
            ls = []
            bagodicts = models.storage.all("Amenity")
            for item in bagodicts.values():
                if item.id in self.amenity_ids:
                    ls.append(item)
            return ls

        @amenities.setter
        def amenities(self, obj):
            """Handles adding an Amenity.id to the attribute amenity_ids"""
            if obj is not None and isinstance(obj, Amenity):
                type(self).amenity_ids.append(obj.id)
