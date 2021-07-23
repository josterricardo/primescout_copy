from django.test import TestCase
import unittest
from . models import  *
from .helpers import ScraperHelper, SeleniumScrapper, json


class ScraperServiceTestCase(TestCase):
    """
    tests the functionality of the service
    existing for gathering the data
    """


class ScraperHelperTestCase(TestCase):
    """
    tests the functionality of the
    helper so that the values
    """