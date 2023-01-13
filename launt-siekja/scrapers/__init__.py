from .scraper import WebScraperBase
from .scraper_t1 import WebScraperT1

WEB_SCRAPERS = {
    "thiessen": WebScraperT1,
}
