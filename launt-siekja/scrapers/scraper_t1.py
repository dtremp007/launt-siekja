from .scraper import WebScraperBase
from urllib.parse import urlencode
import requests
import csv
from bs4 import BeautifulSoup
import time
from request_internal import get_html
from multiprocessing import Pool, Queue, cpu_count, Pipe, Process, Value
import os
import json
from progress.bar import Bar
import math
import inquirer
import datetime
from formatters import FormatterBase
import utils

class WebScraperT1(WebScraperBase):
    def configure(self, website_config, interface, formatter: FormatterBase):
        self.format_internal_filename("thiessen")

        formatter.configure(
                interface,
                source_filename=self.internal_filename,
                seed="thiessen"
            )

        self.url = website_config["url"]
        self.queries = website_config["queries"]
        self.search_path = website_config["search_path"]
        self.formatter = formatter

        return self

    def find_properties(self, session, listing_type, data_queue, properties_total, number_results_reported, properties_written):
        page = 1
        number_results = 1
        links_found = 0

        queries = {key: value for key, value in self.queries.items()
                   if isinstance(value, (str, int, float))}
        queries["type[]"] = listing_type

        while links_found < number_results:
            # Combine the URL, search path, and query to form the full URL
            url = f"{self.url}{replace_page_number(self.search_path, page)}?{urlencode(queries)}"

            html = get_html(session, url)
            soup = BeautifulSoup(html, 'html.parser')

            if page == 1:
                number = soup.find(
                    'h2', class_='rh_page__title').span.text
                number_results = int(number)
                properties_total.value += number_results
                number_results_reported.value += 1

            properties_array = extract_map_data(soup)
            for property in properties_array:
                links_found += 1

                title = property["title"]
                price = property["price"]
                lat = property["lat"]
                lng = property["lng"]
                url = property["url"]
                thumbnail = property["thumb"]

                data_queue.put({"property": [title, price, lat, lng, url, thumbnail, listing_type]})
                properties_written.value += 1

            page += 1
        data_queue.put(None)

    def run(self):
        self.run_scraper()

    def run_scraper(self):
        data_queue = Queue()
        properties_total = Value('i', 0)
        number_results_reported = Value('i', 0)
        properties_written = Value('i', 0)
        processes = []
        for listing_type in self.queries["listing_type"]:
            with requests.Session() as session:
                p = Process(target=self.find_properties, args=(
                    session, listing_type, data_queue, properties_total, number_results_reported, properties_written))
                p.start()
                processes.append(p)

        number_of_processes_completed = 0
        awaiting_reports_progress = Bar('Indexing pages', max=len(processes))
        scraper_progress = None

        awaiting_reports_progress.goto(number_results_reported.value)

        # Create the directory if it doesn't exist
        if not os.path.exists(os.path.dirname(self.internal_filename)):
            os.makedirs(os.path.dirname(self.internal_filename))

        # Open the file for writing
        with open(self.internal_filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            # Add a row to the file
            writer.writerow(['title', 'price', 'lat', 'lng', 'url', 'thumbnail', 'listing_type'])

            # Continuously check if there are any items in the queue
            while number_of_processes_completed < len(processes):
                # If there are no items in the queue, wait for 0.1 seconds before checking again
                if data_queue.empty():
                    time.sleep(0.5)
                    continue

                if number_results_reported.value < len(processes):
                    awaiting_reports_progress.goto(number_results_reported.value)

                if number_results_reported.value == len(processes):
                    awaiting_reports_progress.finish()
                    scraper_progress = Bar('Scraping', max=properties_total.value)
                    scraper_progress.goto(properties_written.value)
                    number_results_reported.value += 1


                # Get an item from the queue
                data = data_queue.get()
                if data is None:
                    number_of_processes_completed += 1
                    continue
                elif "property" in data:
                    writer.writerow(data["property"])
                    if scraper_progress is not None:
                        scraper_progress.goto(properties_written.value)

        for p in processes:
            p.join()



def replace_page_number(url, page_number):
    # Replace the page number with the page number in the URL
    return url.replace('PAGE_NUMBER', str(page_number))


def extract_map_data(soup):
    # Find the script element with the id "property-open-street-map-js-extra"
    script = soup.find("script", {"id": "properties-open-street-map-js-extra"})

    # Extract the "var propertyMapData" from the script
    property_map_data_string = script.text.split( "var propertiesMapData = ")[1].split(";\n")[0]

    return json.loads(property_map_data_string)
