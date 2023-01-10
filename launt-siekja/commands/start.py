import inquirer
import yaml
from scrapers import WebScraperT1, WebScraperBase
from formatters import CSVFormatter


def start(config_file) -> WebScraperBase:
    web_scrapers = {
        "thiessen.com.mx": WebScraperT1,
    }
    formatters = {
        "CSV": CSVFormatter,
    }

    with open(config_file) as f:
        config = yaml.safe_load(f)

    website_choices = [key for key in config["websites"].keys()]

    website = inquirer.list_input(
        message="Which website do you want to scrape?", choices=website_choices)
    format = inquirer.list_input(
        message="What format do want the data in?", choices=formatters.keys())

    website_config = config["websites"][website]

    formatter = formatters[format]()
    scraper = web_scrapers[website](website_config, formatter)
    scraper.configure(website_config)

    return scraper
