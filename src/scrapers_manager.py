import logging
import traceback

from config import *
from disposition import Disposition
from scrapers.rental_offer import RentalOffer
from scrapers.scraper_base import ScraperBase
from scrapers.scraper_bravis import ScraperBravis
from scrapers.scraper_idnes_reality import ScraperIdnesReality
from scrapers.scraper_remax import ScraperRemax
from scrapers.scraper_sreality import ScraperSreality
from scrapers.scraper_ulov_domov import ScraperUlovDomov


def create_scrapers(dispositions: Disposition, min_area: int) -> list[ScraperBase]:
    return [
        ScraperBravis(dispositions, min_area),
        ScraperIdnesReality(dispositions, min_area),
        ScraperRemax(dispositions, min_area),
        ScraperSreality(dispositions, min_area),
        ScraperUlovDomov(dispositions, min_area),
    ]


def fetch_latest_offers(scrapers: list[ScraperBase]) -> list[RentalOffer]:
    """Získá všechny nejnovější nabídky z dostupných serverů

    Returns:
        list[RentalOffer]: Seznam nabídek
    """

    offers: list[RentalOffer] = []
    for scraper in scrapers:
        try:
            for offer in scraper.get_latest_offers():
                offers.append(offer)
        except Exception:
            logging.error(traceback.format_exc())

    return offers
