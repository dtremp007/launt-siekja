class WebScraperBase:
    def __init__(self, url, formatter, internal_filename):
        self.url = url
        self.formatter = formatter
        self.internal_filename = internal_filename

    def run(self):
        pass    # To be implemented by subclasses

    def configure(self, website_config):
        pass    # To be implemented by subclasses

    def export(self):
        self.formatter.export()
