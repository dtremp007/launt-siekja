import datetime
import utils
import os

class WebScraperBase:
    def __init__(self, seed):
        self.seed = seed

    def setup_internal_file(self):
        """
        Formats the internal filename to include the seed and the current date.
        Creates intermediate directories if they don't exist.
        """
        date_string = self.get_date_string()
        self.internal_filename = utils.resolve_path("data", self.seed, f"{self.seed}_{date_string}.csv")
        utils.create_path_if_not_exists(os.path.dirname(self.internal_filename))

    def get_date_string(self):
        return datetime.datetime.now().strftime("%Y-%m-%d")

    def run(self):
        pass    # To be implemented by subclasses

    def configure(self, website_config):
        pass    # To be implemented by subclasses

    def export(self):
        self.formatter.export()
