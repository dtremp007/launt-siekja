import os
import csv
import pandas as pd
from csv_diff import load_csv, compare
from interface import Interface

class FormatterBase:
    def __init__(self):
        self.source_filename = None
        self.previous_filename = None
        self.new_data = []

    def configure(self, interface, source_filename, seed) -> Interface:
        raise NotImplementedError

    def look_for_new_data(self):
        self.sort()
        target_directory = os.path.dirname(self.source_filename)

        with os.scandir(target_directory) as it:
            for entry in it:
                if entry.name.endswith(".csv") and entry.name != os.path.basename(self.source_filename):
                    self.previous_filename = os.path.join(target_directory, entry.name)
                    break

        if self.previous_filename is not None:
            added_data = compare(
                load_csv(open(self.previous_filename), key="id"),
                load_csv(open(self.source_filename), key="id")
            )["added"]
            if len(added_data) > 0:
                self.new_data = pd.DataFrame(added_data)
            else:
                self.new_data = []
            os.remove(self.previous_filename)

    def sort(self):
        pd\
            .read_csv(self.source_filename)\
            .sort_values(by=["title"])\
            .groupby("id", as_index=False)\
            .agg({
                "title": "first",
                "price": "first",
                "lat": "first",
                "lng": "first",
                "url": "first",
                "thumbnail": "first",
                "listing_type": lambda x: ", ".join(x),
                "date_scraped": "first"
            })\
            .fillna("")\
            .to_csv(self.source_filename, index=False)


    def export(self):
        raise NotImplementedError
