from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class EventBooking(Base):
    """ Event Booking """

    __tablename__ = "event_booking"

    id = Column(Integer, primary_key=True)
    member_id = Column(String(250), nullable=False)
    club_id = Column(String(250), nullable=False)
    event_id = Column(String(250), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, member_id, club_id, event_id, timestamp):
        """ Initializes an event booking """
        self.member_id = member_id
        self.club_id = club_id
        self.event_id = event_id
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of an event booking """
        dict = {}
        dict['id'] = self.id
        dict['member_id'] = self.member_id
        dict['club_id'] = self.club_id
        dict['event_id'] = self.event_id
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created

        return dict
