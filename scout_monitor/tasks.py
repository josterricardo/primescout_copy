from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings
from celery.utils.log import get_task_logger
from scout_monitor.helpers import ScraperHelper
import datetime
import os
from .management.commands.fetch_data_from_site import Command

SCRAPER_HANDLER = ScraperHelper()

logger = get_task_logger(__name__)

@shared_task
def load_product_data_to_db():
    """
    Loads the data coming from the scraper itself
    into the DB which could be used for later purposes

    :return: None
    """
    result = SCRAPER_HANDLER.fetch_data_for_db()
    if not result['status']:
        logger.error(f"{result['error']}")
        # import pdb; pdb.set_trace()
        raise Exception(result['error'])

    else:
        logger.info(f"The task was performed successfully.")


@shared_task
def fetch_site_data():
    """
    fetches the data from the file and
    generates a json with it
    :return:None
    """
    executer = Command()
    # file = f"/home/ubuntu/prime_scout/scraped_site_data_{datetime.datetime.now().isoformat()}.json"
    file = f"/home/virus-enabled/Desktop/scraped_site_data_{datetime.datetime.now().isoformat()}.json"
    result = executer.handle(file_path=file)

    if not result:
        logger.error(f"Ther was an error with the fetching request. check the logs")
        raise Exception(result['error'])

    else:
        logger.info(f"The task was performed successfully.")
