from .formatter import FormatterBase
import os
import csv
import shutil
import utils
import yaml

OUTPUT_DIR = "~/Documents/launt-siekja"

class CSVFormatter(FormatterBase):
    def configure(self, interface, source_filename, seed):
        def assign_variables(user_settings):
            self.source_filename = source_filename
            self.output_filename = os.path.join(user_settings["output_directory"], f"{seed}.csv")

        interface\
            .path(
                "output_directory",
                "Where do you want to store the data?",
                os.path.expanduser(OUTPUT_DIR),
                True
            )\
            .queue_handler(assign_variables)

    def export(self):
        self.look_for_new_data()

        utils.create_path_if_not_exists(os.path.dirname(self.output_filename))

        if self.previous_filename == None or os.path.exists(self.output_filename) == False:
            shutil.copyfile(self.source_filename, self.output_filename)
            return

        if os.path.exists(self.output_filename) and len(self.new_data) > 0:
            with open(self.output_filename, "a") as f:
                writer = csv.DictWriter(f, fieldnames=self.new_data[0].keys())

                for row in self.new_data:
                    writer.writerow(row)

        print(f"\nFile has been saved to {self.output_filename}")
