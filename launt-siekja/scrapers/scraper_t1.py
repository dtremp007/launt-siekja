from .scraper import WebScraperBase
from urllib.parse import urlencode
import requests
import csv
from bs4 import BeautifulSoup
import time
from request_internal import get_html
from multiprocessing import Pool, Queue, cpu_count, Pipe, Process, Value, Manager, Lock
import os
import json
from progress.bar import Bar
import math
import inquirer
import datetime
from formatters import FormatterBase
import utils


class WebScraperT1(WebScraperBase):
    def __init__(self):
        super().__init__("thiessen")

    def configure(self, website_config, interface, formatter: FormatterBase):
        self.url = website_config["url"]
        self.queries = website_config["queries"]
        self.search_path = website_config["search_path"]
        self.results_per_page = website_config["results_per_page"]
        self.formatter = formatter
        self.results = None

        return self

    def search_by_category(self, session, listing_type, queue):
        page_number = 1
        max_pages = 1
        while page_number <= max_pages:
            soup = self.get_soup(
                session,
                self.get_search_url(
                    page_number,
                    self.parse_queries(listing_type)))

            # if page_number == 1:
            #     number_results = self.extract_search_results_number(soup)
            #     max_pages = math.ceil(number_results / self.results_per_page)

            self.scrape_search_results(soup, listing_type, queue)
            page_number += 1

        queue.put(None)

    def parse_queries(self, listing_type):
        queries = {key: value for key, value in self.queries.items()
                        if isinstance(value, (str, int, float))}
        queries["type[]"] = listing_type
        return urlencode(queries)

    def get_soup(self, session, url):
        html = get_html(session, url)
        return BeautifulSoup(html, 'html.parser')

    def get_search_url(self, page_number, query_string):
        return f"{self.url}{self.replace_page_number(self.search_path, page_number)}?{query_string}"

    def scrape_search_results(self, soup, listing_type, queue):
        properties_array = self.extract_map_data(soup)

        for property in properties_array:
            title = property["title"]
            price = property["price"]
            lat = property["lat"]
            lng = property["lng"]
            url = property["url"]
            thumbnail = property["thumb"]

            data = [title, price, lat, lng, url, thumbnail, listing_type]
            queue.put(data)


    def extract_search_results_number(self, soup):
        number = soup.find(
            'h2', class_='rh_page__title').span.text
        number_results = int(number)
        return number_results

    def run(self):
        if not os.path.exists(self.internal_filename):
            self.run_scraper()
        return self

    def run_scraper(self):
        processes = []
        queue = Queue()
        queues_reported = 0
        self.create_csv()
        for listing_type in self.queries["listing_type"]:
            with requests.Session() as session:
                p = Process(target=self.search_by_category, args=(session, listing_type, queue))
                p.start()
                processes.append(p)

        awaiting_processes = Bar('Scraping pages', max=len(processes))

        with open(self.internal_filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            # Add a row to the file
            writer.writerow(['title', 'price', 'lat', 'lng',
                            'url', 'thumbnail', 'listing_type'])

            while queues_reported < len(processes):
                data = queue.get()
                if data is None:
                    queues_reported += 1
                    awaiting_processes.next()
                else:
                    writer.writerow(data)

        for p in processes:
            p.join()

        # awaiting_processes.finish()

    def create_csv(self):
        # Open the file for writing
        with open(self.internal_filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            # Add a row to the file
            writer.writerow(['title', 'price', 'lat', 'lng',
                            'url', 'thumbnail', 'listing_type'])


    def add_result(self, id, data):
        if self.results and id not in self.results:
            self.results[id] = data


    def replace_page_number(self, url, page_number):
        # Replace the page number with the page number in the URL
        return url.replace('PAGE_NUMBER', str(page_number))


    def extract_map_data(self, soup):
        # Find the script element with the id "property-open-street-map-js-extra"
        script = soup.find("script", {"id": "properties-open-street-map-js-extra"})

        # Extract the "var propertyMapData" from the script
        property_map_data_string = script.text.split(
            "var propertiesMapData = ")[1].split(";\n")[0]

        return json.loads(property_map_data_string)
