import inquirer
import yaml
from scrapers import WEB_SCRAPERS, WebScraperBase
from formatters import FORMATTERS


def start(config_file, interface) -> WebScraperBase:
    with open(config_file) as f:
        config = yaml.safe_load(f)

    def setup_and_run_scraper(answers):
        website = answers["website"]
        format = answers["format"]
        website_config = config["websites"][website]

        scraper = WEB_SCRAPERS[website]()
        formatter = FORMATTERS[format]()

        scraper.setup_internal_file()

        formatter\
            .configure(
                interface,
                source_filename=scraper.internal_filename,
                seed=scraper.seed
            )

        scraper\
            .configure(
                website_config,
                interface,
                formatter
            )

        interface\
            .execute()
        scraper\
            .run()\
            .export()


    website_choices = [key for key in WEB_SCRAPERS.keys()]
    formatter_choices = [key for key in FORMATTERS.keys()]

    interface\
        .parse_args()\
        .select(
            "website",
            "Which website do you want to scrape?",
            website_choices,
            website_choices[0]
        )\
        .select(
            "format",
            "How do you want to export the data?",
            formatter_choices,
            formatter_choices[0]
        )\
        .queue_handler(setup_and_run_scraper)\
        .execute()
