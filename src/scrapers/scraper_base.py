import re
from abc import abstractmethod
from typing import Any

from requests import Response

from disposition import Disposition
from scrapers.rental_offer import RentalOffer
from utils import flatten


class ScraperBase():
    """Hlavní třída pro získávání aktuálních nabídek pronájmu bytů z různých služeb
    """

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    headers = {"User-Agent": user_agent}
    area_regex = re.compile(r"(?P<area>\d+)\s*m[²2]")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def logo_url(self) -> str:
        pass

    @property
    @abstractmethod
    def color(self) -> int:
        pass

    @property
    @abstractmethod
    def disposition_mapping(self) -> dict[Disposition, Any]:
        pass

    def __init__(self, disposition: Disposition, min_area: int) -> None:
        self.disposition = disposition
        self.min_area = min_area

    def get_dispositions_data(self) -> list:
        return list(flatten([self.disposition_mapping[d] for d in self.disposition]))

    def is_area_sufficient(self, area_string: str) -> bool:
        match = self.area_regex.search(area_string)
        area = int(match.group("area"))
        return not area or area >= self.min_area

    @abstractmethod
    def build_response() -> Response:
        """Vytvoří a pošle dotaz na server pro získání nabídek podle nakonfigurovaných parametrů

        Raises:
            NotImplementedError: Pokud potomek neimplementuje tuto metodu

        Returns:
            Response: Odpověď nabídkového serveru obsahující neparsované nabídky
        """
        raise NotImplementedError("Server request builder is not implemeneted")

    @abstractmethod
    def get_latest_offers() -> list[RentalOffer]:
        """Načte a vrátí seznam nejnovějších nabídek bytů k pronájmu z dané služby

        Raises:
            NotImplementedError: Pokud potomek neimplementuje tuto metodu

        Returns:
            list[RentalOffer]: Seznam nabízených bytů k pronájmu
        """
        raise NotImplementedError("Fetching new results is not implemeneted")
