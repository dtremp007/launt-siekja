from .formatter import FormatterBase
import os
import csv
import shutil

class CSVFormatter(FormatterBase):


    def export(self):
        self.look_for_new_data()
        if self.previous_filename == None or os.path.exists(self.output_filename) == False:
            shutil.copyfile(self.source_filename, self.output_filename)
            return

        if os.path.exists(self.output_filename) and len(self.new_data) > 0:
            with open(self.output_filename, "a") as f:
                writer = csv.DictWriter(f, fieldnames=self.new_data[0].keys())

                for row in self.new_data:
                    writer.writerow(row)

        print(f"\nFile has been saved to {self.output_filename}")
