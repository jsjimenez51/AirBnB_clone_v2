#!/usr/bin/python3
"""
Module defines  DB storage
"""
import json
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import models


class DBStorage:
    """
    Defines DBstorage class
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        initializes the db storage engine
        """
        usr = getenv('HBNB_MYSQL_USER')
        pswd = getenv('HBNB_MYSQL_PWD')
        hst = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                usr, pswd, hst, db, pool_pre_ping=True))

        Base.metadata.create_all(self.__engine)

        if getenv('HBNB_MYSQL_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of all classes requested
        """
        all_dicts = {}
        if cls is not None:
            objects = self.__session.query(models.classes[cls]).all()
            for obj in objects:
                key = obj.__class__.__name__ + "." + obj.id
                all_dicts[key] = obj
            return all_dicts
        else:
            # Checks class for BaseModel as an excemption otherwise
            # Checks all classes
            for key, value in models.classes.items():
                if key != "BaseModel":
                    objects = self.__session.query(value).all()
                    for obj in objects:
                        table = obj.__class__.__name__ + "." + obj.id
                        all_dicts[table] = obj
            return all_dicts

    def new(self, obj):
        """
        creates a new object for current session
        """
        self.__session.add(obj)

    def save(self):
        """
        saves object to database
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        deletes object from database
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        creates a new session and loads object from database
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))()

    def close(self):
        """ Calls the remove method on the current session to close it
        """
        self.__session.close()
