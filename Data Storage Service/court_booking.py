from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class CourtBooking(Base):
    """ Court Booking """

    __tablename__ = "court_booking"

    id = Column(Integer, primary_key=True)
    member_id = Column(String(250), nullable=False)
    member_id_2 = Column(String(250), nullable=False)
    club_id = Column(String(250), nullable=False)
    court_num = Column(Integer, nullable=False)
    booking_time = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, member_id, member_id_2, club_id, court_num, booking_time, duration, timestamp):
        """ Initializes a court booking """
        self.member_id = member_id
        self.member_id_2 = member_id_2
        self.club_id = club_id
        self.court_num = court_num
        self.booking_time = booking_time
        self.duration = duration
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a court booking """
        dict = {}
        dict['id'] = self.id
        dict['member_id'] = self.member_id
        dict['member_id_2'] = self.member_id_2
        dict['club_id'] = self.club_id
        dict['court_num'] = self.court_num
        dict['booking_time'] = self.booking_time
        dict['duration'] = self.duration
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created

        return dict
