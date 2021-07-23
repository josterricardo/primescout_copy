import json
import os
import sys
import warnings
from datetime import datetime
from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.utils.timezone import make_aware
from django.conf import settings
from scout_monitor_fetcher.SeleniumScrapper import SeleniumScrapper


class Command(BaseCommand):

    def add_arguments(self, parser):
        """
        adds arguments for the console parser, so that different options required
        with the command are capable of being processed
        :param parser: ArgumentParser object
        :return: None
        """
        parser.add_argument(
            "file_path",
            type=str,
            help="path of the file to be load the data onto"
        )

    def handle(self, **options):
        """
        handles the commands prompted through the terminal or any type of call
        :param options: dict: dictionary containing the keyword
         arguments needed for the operations
        :return: None
        """
        if options.get("file_path") is not None:
            file = options.get('file_path')
            scrapper = SeleniumScrapper()
            result = scrapper.scrape_items()
            if result['status']:
                with open(file,'w') as dumper:
                    dumper.write("[\n")
                    for data in result['data']:
                        dumper.write(json.dumps(data)+", \n")
                    dumper.write("]")
                dumper.close()
                self.stdout.write(self.style.SUCCESS(f"{result['message']}" ))
                return result['status']

            else:
                self.stdout.write(self.style.ERROR(f"{result['error']}" ))
                return result['status']

        else:
            self.stderr.write("you must provide the path where the data will be stored to make this work.")
        exit(0)



