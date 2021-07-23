# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
# from items import *
import requests as req
import bs4


class AlkostoSpider(scrapy.Spider):
    name = 'alkosto'
    allowed_domains = ['*']
    start_urls = ['https://www.alkosto.com/electro/neveras/neveras']

    # def make_requests_from_url(self, url):
    #     """
    #     creates a request for the existing url
    #     but in fact I'm just going to generate requests
    #     based on each item belonging in the link because
    #     there are X amount of objects I could use.
    #     :param url: str
    #     :return: response to the parse method
    #     """
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse, method='GET')



    def parse(self, response, **kwargs):
        """

        :param response:
        :param kwargs:
        :return:
        """
        pages = []
        select = Selector(response=response, type='html')
        page_obj = select.css("div[class~='wrapper']").css('div.page')
        res = req.get(self.start_urls[0], timeout=100)
        res_body = ''.join(page_obj.extract()).replace('\r','').replace('\n','').replace('\t','')
        alternate_selector = Selector(text=res_body, type='html')
        for div in alternate_selector.xpath('//div'):
            print(div.attrib)

        import pdb;pdb.set_trace()


    def parse_product_data(self, response, **kwargs):
        """
        this generates a request which should be processed in a way
        that it goes to each part of the site to gather the resources like:
        -images
        -descriptions
        -reviews
        :param response:
        :param kwargs:
        :return:item
        """

    def parse_page_reviews(self, paginated_data_response):
        """
        gets each review in the paginated page which is
        basically the url that follows all of the data
        :param paginated_data_response: scrapy response
        :return: list of dicts
        """


    def get_review_score(self,star_items):
        """
        generates the review score based on the existing
        stars one full star +1, an empty star: -1
        :param star_items: items
        :return: int
        """



    def parse_product_details(self, details_item):
        """
        gets the details from the table for the
        item description
        :param details_item: selector
        :return: dict
        """


