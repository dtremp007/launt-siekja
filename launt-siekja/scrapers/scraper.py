class WebScraperBase:
    def __init__(self, url, format, output_filename, internal_filename):
        self.url = url
        self.format = format
        self.output_filename = output_filename
        self.internal_filename = internal_filename

    def run(self):
        pass    # To be implemented by subclasses

    def configure(self, website_config):
        pass    # To be implemented by subclasses
