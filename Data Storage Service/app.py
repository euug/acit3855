import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
import create_tables_mysql
from court_booking import CourtBooking
from event_booking import EventBooking
from events import Events
from datetime import datetime
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
import yaml
import json
import logging
import logging.config

# External Application Configuration
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

# External Logging Configuration
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine('mysql+pymysql://%s:%s@%s:%d/%s' % (
                                app_config["datastore"]["user"],
                                app_config["datastore"]["password"],
                                app_config["datastore"]["hostname"],
                                app_config["datastore"]["port"],
                                app_config["datastore"]["db"]))

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

logger.info("Connecting to DB, Hostname:%s, Port:%s" % (app_config["datastore"]["hostname"], app_config["datastore"]["port"]))

def get_court_bookings(timestamp):
    """ Gets new court bookings after the timestamp """
    session = DB_SESSION()
    
    timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    
    bookings = session.query(CourtBooking).filter(CourtBooking.date_created >= timestamp_datetime)
    
    results_list = []
    
    for booking in bookings:
        results_list.append(booking.to_dict())
    
    session.close()
    
    logger.info("Query for Court Bookings after %s returns %d results" % (timestamp, len(results_list)))
    
    return results_list, 200

def get_event_bookings(timestamp):
    """ Gets new event bookings after the timestamp """
    session = DB_SESSION()
    
    timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    
    bookings = session.query(EventBooking).filter(EventBooking.date_created >= timestamp_datetime)
    
    results_list = []
    
    for booking in bookings:
        results_list.append(booking.to_dict())
    
    session.close()
    
    logger.info("Query for Event Bookings after %s returns %d results" % (timestamp, len(results_list)))
    
    return results_list, 200

def store_court_booking(body):
    session = DB_SESSION()

    e = Events(json.dumps(body))

    session.add(e)

    session.commit()
    session.close()

    logger.debug('Stored court booking payload')

    return NoContent, 201

def store_event_booking(body):
    session = DB_SESSION()

    e = Events(json.dumps(body))

    session.add(e)

    session.commit()
    session.close()

    logger.debug('Stored event booking payload')

    return NoContent, 201

def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]

    # Create and consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts
    consumer = topic.get_simple_consumer(consumer_group='event_group',
                                        reset_offset_on_start=False,
                                        auto_offset_reset=OffsetType.LATEST)
    
    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)

        payload = msg["payload"]

        if msg["type"] == "court_booking":
            store_court_booking(payload)
        elif msg["type"] == "event_booking":
            store_event_booking(payload)
    
        consumer.commit_offsets()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()

    app.run(port=8090)