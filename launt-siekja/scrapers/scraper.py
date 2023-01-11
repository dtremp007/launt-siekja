import datetime
import utils
import os

class WebScraperBase:


    def format_internal_filename(self, seed):
        """
        Formats the internal filename to include the seed and the current date.
        Creates intermediate directories if they don't exist.
        """
        date_string = datetime.datetime.now().strftime("%Y-%m-%d")
        self.internal_filename = utils.resolve_path("data", seed, f"{seed}_{date_string}.csv")
        utils.create_path_if_not_exists(os.path.dirname(self.internal_filename))

    def run(self):
        pass    # To be implemented by subclasses

    def configure(self, website_config):
        pass    # To be implemented by subclasses

    def export(self):
        self.formatter.export()
