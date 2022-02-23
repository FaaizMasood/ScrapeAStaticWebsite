#!/usr/bin/env python3

import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.common.exceptions import NoSuchElementException


# Rule is new parameter for crawl spider
# Rule takes in 3 parameters, a function that is LinkExtractor(imported above) , a call back and a follow boolean(-
# if true then goes on all pages and extract if false then stops at the first page-)
# LinkExtractor(deny_domains=('google.com')) is added to avoid certail pages
# LinkExtractor(allow=('google.com')) is added and it will check all the url for this word
# class BooksSpider(CrawlSpider):
#     name = 'books'
#     allowed_domains = ['books.toscrape.com/']
#     # Removed www because can cause errors
#     start_urls = ['http://books.toscrape.com/']
#     rules = (Rule(LinkExtractor(deny_domains=('google.com')),
#              callback='parse_page', follow=False),)

#     def parse(self, response):
#         pass


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com/']

    # spider attribute
    def start_requests(self):
        #s = Service('/Users/faaizmasood/ScrapeAStaticWebsite/chromedriver.exe')
        self.driver = webdriver.Chrome()
        self.driver.get('http://books.toscrape.com')
        sel = Selector(text=self.driver.page_source)  # selector is from scrapy
        books = sel.xpath('//h3/a/@href').extract()
        for book in books:
            url = 'http://books.toscrape.com/' + book
            yield Request(url, callback=self.parse_book)
        while True:
            try:
                next_page = self.driver.find_element_by_xpath(
                    '//a[text()="next"]')
                sleep(3)
                self.logger.info('Sleeping for 3 secs')
                next_page.click()

                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()
                for book in books:
                    url = 'http://books.toscrape.com/' + book
                    yield Request(url, callback=self.parse_book)
            except NoSuchElementException:
                self.logger.info('No More Pages Faaiz')
                self.driver.quit()
                break

    def parse_book(self, response):
        pass
