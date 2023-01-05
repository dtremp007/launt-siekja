import yaml
from typing import List

class Config:
    def __init__(self, config_file):
        with open(config_file) as f:
            config = yaml.safe_load(f)
        self.__dict__.update(config)

    def set_website(self, website):
        self.website = website
        self.url = self[website]["url"]
