import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

def get_court_booking_info(index):
    """ Get Court Booking in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                        consumer_timeout_ms=100)
    
    logger.info("Retrieving court booking at index %d" % index)

    count = 0
    reading = None
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)

        if msg["type"] == "court_booking":
            if count == index:
                reading = msg["payload"]
                return reading, 200
            
            count += 1
    
    logger.error("Could not find court booking at index %d" % index)
    return { "message": "Not Found"}, 404

def get_event_booking_info(index):
    """ Get Event Booking in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]

    consumer = topic.getsimple_consumer(reset_offset_on_start=True,
                                        consumer_timeout_ms=100)
    
    logger.info("Retrieving event booking at index %d" % index)

    count = 0
    reading = None
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)

        if msg["type"] == "event_booking":
            if count == index:
                reading = msg["payload"]
                return reading, 200
            
            count += 1
    
    logger.error("Could not find event booking at index %d" % index)
    return { "message": "Not Found"}, 404

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8110)