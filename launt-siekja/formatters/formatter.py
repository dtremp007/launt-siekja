import os
import csv
import pandas as pd
from csv_diff import load_csv, compare

class FormatterBase:
    def __init__(self):
        self.source_filename = None
        self.new_data = []
        self.previous_filename = None

    def set_source(self, source_filename):
        self.source_filename = source_filename

    def set_output(self, output_filename):
        self.output_filename = output_filename

    def look_for_new_data(self):
        self.sort()
        target_directory = os.path.dirname(self.source_filename)

        with os.scandir(target_directory) as it:
            for entry in it:
                if entry.name.endswith(".csv") and entry.name != os.path.basename(self.source_filename):
                    self.previous_filename = os.path.join(target_directory, entry.name)
                    break

        if self.previous_filename is not None:
            self.new_data = compare(
                load_csv(open(self.previous_filename), key="title"),
                load_csv(open(self.source_filename), key="title")
            )["added"]
            os.remove(self.previous_filename)

    def sort(self):
        pd.read_csv(self.source_filename).sort_values(by=["title"]).to_csv(self.source_filename, index=False)


    def export(self):
        raise NotImplementedError

    def configure(self):
        raise NotImplementedError