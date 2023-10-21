#!/usr/bin/python3
""" c'est la module pour la classe state pour le projet HBNB """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ c'est la classe state """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship(
                "City",
                backref="state",
                cascade="all, delete-orphan"
                )
    else:
        @property
        def cities(self):
            """It's Getter attribute that returns the list of Cit
            instances with state_id equals to the current State.id
            """
            from models import storage
            result = []
            for city in storage.all("City").values():
                if city.state_id == self.id:
                    result.append(city)
            return result
