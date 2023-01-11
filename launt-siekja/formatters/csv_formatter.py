from .formatter import FormatterBase
import os
import csv
import shutil
import utils
import yaml

class CSVFormatter(FormatterBase):
    def configure(self, interface, source_filename, seed):
        user_settings = {}
        user_settings_filename = utils.resolve_path("user_settings.yaml")
        try:
            with open(user_settings_filename) as f:
                user_settings = yaml.safe_load(f)
        except FileNotFoundError:
            pass

        if "output_directory" not in user_settings:
            user_settings["output_directory"] = os.path.expanduser("~/Documents/launt-siekja")

        self.source_filename = source_filename
        self.output_filename = utils.resolve_path(user_settings["output_directory"], f"{seed}.csv")

        with open(user_settings_filename, "w") as f:
            yaml.dump(user_settings, f)


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
