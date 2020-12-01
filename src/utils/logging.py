import datetime
import logging
import os
import traceback
import pytz

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.CRITICAL, filename=os.path.join(BASE_DIR, 'logging_critical.log'))
logging.basicConfig(level=logging.ERROR, filename=os.path.join(BASE_DIR, 'logging_error.log'))
logging.basicConfig(level=logging.INFO, filename=os.path.join(BASE_DIR, 'logging_info.log'))


def add_logging_critical():
    """Logging for critical events."""
    now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
    date_and_time = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    logging.critical('{0}: {1}'.format(date_and_time, traceback.format_exc()))


def add_logging_error():
    """Logging for error events."""
    now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
    date_and_time = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    logging.error('{0}: {1}'.format(date_and_time, traceback.format_exc()))


def add_logging_info():
    """Logging for error events."""
    now = datetime.datetime.now(pytz.timezone('Europe/Stockholm'))
    date_and_time = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    logging.info('{0}: {1}'.format(date_and_time, traceback.format_exc()))


