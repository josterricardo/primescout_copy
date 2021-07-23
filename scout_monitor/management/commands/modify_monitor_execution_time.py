import json
import os
import sys
import warnings
from datetime import datetime
from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.utils.timezone import make_aware
from django.conf import settings
import pytz
from scout_monitor_fetcher.SeleniumScrapper import SeleniumScrapper
from django_celery_beat.models import PeriodicTask, CrontabSchedule,TzAwareCrontab


class Command(BaseCommand):

    def add_arguments(self, parser):
        """
        adds arguments for the console parser, so that different options required
        with the command are capable of being processed
        :param parser: ArgumentParser object
        :return: None
        """
        parser.add_argument(
            "new_execution_time",
            type=int,
            help="this execution time will change the DB which represents how many hours it a day it should be run."
                 " it only accepts integers from 0-23"
        )

        parser.add_argument(
            "new_execution_time_minutes",
            type=int,
            help="this execution time will change the DB which represents how many hours it a day it should be run."
                 " it only accepts integers from 1-59"
        )

    def handle(self, **options):
        """
        handles the commands prompted through the terminal or any type of call
        :param options: dict: dictionary containing the keyword
         arguments needed for the operations
        :return: None
        """
        scheduled_task_name = "populate_db_from_site"
        if options.get("new_execution_time") is not None:
            new_exec_time = options.get('new_execution_time')
            new_exec_time_minutes = options.get('new_execution_time_minutes')

            tz = pytz.timezone('America/New_York')
            try:
                if new_exec_time > 23 or new_exec_time < 0 or new_exec_time_minutes > 59 or new_exec_time_minutes < 1:
                    raise Exception("The execution time range must be between: HOURS: 0 - 23 / MINUTES: 1 - 59")

                scheduled_task = PeriodicTask.objects.get(name=scheduled_task_name)
                new_exec, created = CrontabSchedule.objects.get_or_create(
                    minute=f'{new_exec_time_minutes}',
                hour = f'*/{new_exec_time}',
                day_of_week = '*',
                day_of_month = '0',
                month_of_year = '0',
                timezone=tz
                )
                scheduled_task.crontab = new_exec
                scheduled_task.save()
                self.stdout.write(self.style.SUCCESS(f"The New Execution time"
                                                     f" for the data fetcher is every {new_exec_time} "
                         f"{'hours' if new_exec_time > 1 else 'hour'}" ))

            except Exception as X:
                self.stdout.write(self.style.ERROR(f"There was an error while trying to update the execution time:"
                                                   f"{X}" ))
        else:
            self.stderr.write("you must provide the path where the data will be stored to make this work.")
        exit(0)



