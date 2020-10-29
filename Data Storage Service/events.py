from sqlalchemy import Column, Integer, String
from base import Base

class Events(Base):
    """ Events """

    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    payload = Column(String(250), nullable=False)

    def __init__(self, payload):
        """ Initializes an events """
        self.payload = payload