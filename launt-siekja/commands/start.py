import inquirer
import yaml
from scrapers import WebScraperT1, WebScraperBase


def start(config_file) -> WebScraperBase:
    web_scrapers = {
        "thiessen.com.mx": WebScraperT1,
    }

    with open(config_file) as f:
        config = yaml.safe_load(f)

    website_choices = [key for key in config["websites"].keys()]

    website = inquirer.list_input(
        message="Which website do you want to scrape?", choices=website_choices)
    format = inquirer.list_input(
        message="What format do want the data in?", choices=config["formats"])

    website_config = config["websites"][website]

    scraper = web_scrapers[website](website_config, format)

    return scraper
