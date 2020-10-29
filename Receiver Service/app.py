import connexion
from connexion import NoContent
import requests
from datetime import datetime
import yaml
import logging
import logging.config
import json
from pykafka import KafkaClient

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def report_court_booking(body):

    logger.info(f'Received court booking for court #{body["court_num"]} from member with ID# {body["member_id"]}')

    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config['events']['topic']]
    producer = topic.get_sync_producer()
    msg = { "type": "court_booking",
            "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f'Returned court booking for court #{body["court_num"]} response (member ID# {body["member_id"]}')

    return NoContent, 201

def report_event_booking(body):

    logger.info(f'Received event booking for club {body["club_id"]} with unique event ID# {body["event_id"]}')
  
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config['events']['topic']]
    producer = topic.get_sync_producer()
    msg = { "type": "event_booking",
            "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f'Returned event booking for club {body["club_id"]} response (event ID# {body["event_id"]}')

    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":    app.run(port=8080)