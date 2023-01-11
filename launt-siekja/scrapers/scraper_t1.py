from .scraper import WebScraperBase
from urllib.parse import urlencode
import requests
import csv
from bs4 import BeautifulSoup
import time
from request_internal import get_html
from multiprocessing import Pool, Queue, cpu_count, Pipe, Process, Value, Manager
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
        self.formatter = formatter
        self.results = None

        return self

    def search_by_category(self, session, listing_type):
        page_number = 1
        max_pages = 1

        query_string = self.parse_queries(listing_type)

        while links_found < max_pages:
            self.scrape_search_results(page_number)

        data_queue.put(None)

    def parse_queries(self, listing_type):
        queries = {key: value for key, value in self.queries.items()
                        if isinstance(value, (str, int, float))}
        queries["type[]"] = listing_type
        return urlencode(queries)

    def scrape_search_results(self, page_number, query_string, listing_type):
        # Combine the URL, search path, and query to form the full URL
        url = f"{self.url}{replace_page_number(self.search_path, page_number)}?{query_string}"

        html = get_html(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        properties_array = extract_map_data(soup)

        for property in properties_array:
            title = property["title"]
            price = property["price"]
            lat = property["lat"]
            lng = property["lng"]
            url = property["url"]
            thumbnail = property["thumb"]

            data = [title, price, lat, lng, url, thumbnail, listing_type]
            self.add_result(title, data)


    def extract_search_results_number(self, soup):
        number = soup.find(
            'h2', class_='rh_page__title').span.text
        number_results = int(number)
        properties_total.value += number_results
        return number_results

    def run(self):
        self.run_scraper()
        return self

    def run_scraper(self):
        properties_total = Value('i', 0)
        properties_written = Value('i', 0)
        processes = []
        with Manager() as manager:
            for listing_type in self.queries["listing_type"]:
                self.results = manager.dict()
                with requests.Session() as session:
                    p = Process(target=self.search_by_category, args=(
                        session, listing_type, data_queue, properties_total, number_results_reported, properties_written))
                    p.start()
                    processes.append(p)

        number_of_processes_completed = 0
        awaiting_reports_progress = Bar('Indexing pages', max=len(processes))
        scraper_progress = None

        awaiting_reports_progress.goto(number_results_reported.value)

        # Open the file for writing
        with open(self.internal_filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            # Add a row to the file
            writer.writerow(['title', 'price', 'lat', 'lng',
                            'url', 'thumbnail', 'listing_type'])


        for p in processes:
            p.join()

    def add_result(self, id, data):
        if self.results and id not in self.results:
            self.results[id] = data


def replace_page_number(url, page_number):
    # Replace the page number with the page number in the URL
    return url.replace('PAGE_NUMBER', str(page_number))


def extract_map_data(soup):
    # Find the script element with the id "property-open-street-map-js-extra"
    script = soup.find("script", {"id": "properties-open-street-map-js-extra"})

    # Extract the "var propertyMapData" from the script
    property_map_data_string = script.text.split(
        "var propertiesMapData = ")[1].split(";\n")[0]

    return json.loads(property_map_data_string)
