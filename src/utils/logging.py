import datetime
import logging
import traceback

import pytz

logging.basicConfig(level=logging.CRITICAL, filename='critical_errors.log')
logging.basicConfig(level=logging.ERROR, filename='error_errors.log')


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


