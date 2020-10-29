import connexion
from connexion import NoContent
from apscheduler.schedulers.background import BackgroundScheduler
import requests

import datetime
import yaml
import json
import logging
import logging.config
import os.path

# External Application Configuration
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

# External Logging Configuration
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def populate_stats():
    """ Periodically update stats """
    logger.info("Start Periodic Processing")

    # Get current stats loaded into the variables
    if os.path.isfile(app_config['datastore']['filename']):
        with open(app_config['datastore']['filename']) as f:
            stats = json.loads(f.read())

        num_court_bookings = stats['num_court_bookings']
        max_num_courts = stats['max_num_courts']
        total_hours_booked = stats['total_hours_booked']
        num_event_bookings = stats['num_event_bookings']
        timestamp = stats['timestamp']
    else:
        # Initialize variables
        num_court_bookings = 0
        max_num_courts = 0
        total_hours_booked = 0
        num_event_bookings = 0
        timestamp = "2020-09-10T08:30:00Z"
    
    # Create timestamp
    raw_time = datetime.datetime.now()
    curr_time = datetime.datetime.strftime(raw_time, "%Y-%m-%dT%H:%M:%SZ")

    # Send get request with timestamp as parameter
    response_cb = []
    response_eb = []

    response_cb = requests.get(app_config['eventstore']['url'] + '/report/court-booking', params={'timestamp':timestamp})
    response_eb = requests.get(app_config['eventstore']['url'] + '/report/event-booking', params={'timestamp':timestamp})

    if response_cb.status_code == 200:
        # Calculate how many bookings are received
        len_cb = len(response_cb.json())
        len_eb = len(response_eb.json())
        # log number of bookings received
        logger.info(f'{len_cb} new court bookings and {len_eb} new event bookings')
    else:
        # log error if no response returned
        logger.error('Could not get new stats')

    # Calculate new statistics
    for i in response_cb.json():
        num_court_bookings += 1

        if i['court_num'] > max_num_courts:
            max_num_courts = i['court_num']
        
        total_hours_booked = total_hours_booked + i['duration']
        
    for j in response_eb:
        num_event_bookings += 1
    
    # Put results as dictionary
    stats_dict = {}
    stats_dict['num_court_bookings'] = num_court_bookings
    stats_dict['max_num_courts'] = max_num_courts
    stats_dict['total_hours_booked'] = total_hours_booked
    stats_dict['num_event_bookings'] = num_event_bookings
    stats_dict['timestamp'] = curr_time

    with open('stats.json', 'w') as f:
        json.dump(stats_dict, f)
    
    logger.debug(f'Total number of court bookings: {num_court_bookings}, Max number of courts in a club: {max_num_courts}, Total hours booked: {total_hours_booked}, Total number of event bookings: {num_event_bookings}')

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                'interval',
                seconds=app_config['scheduler']['period_sec'])
    sched.start() 

def get_stats():
    """ Gets stats from json file """
    logger.info('Start GET stats request.')

    if os.path.isfile('./stats.json'):
        with open('stats.json') as f:
            stats = json.loads(f.read())
    else:
        logger.error('Statistics do not exist.')
        return 404

    logger.debug(f'Stats received: {stats}')
    logger.info('Request complete')

    return stats, 200


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)