import pandas as pd

from atlas.domain.stock.port.kospi_constituents_cache import (
    KospiConstituentsCachePort,
)
from atlas.domain.stock.port.kospi_constituents_raw import (
    KospiConstituentsRawPort,
)

class KospiConstituentsService:
    def __init__(
            self,
            raw: KospiConstituentsRawPort,
            cache: KospiConstituentsCachePort,
    ):
        self.raw = raw
        self.cache = cache

    def build(self) -> pd.DataFrame:
        if not self.raw.exists():
            raise FileNotFoundError("KOSPI constituents raw file not found.")

        df = self.raw.read()
        self.cache.save(df)

        return df

    def read(self) -> pd.DataFrame:
        if not self.cache.exists():
            raise FileNotFoundError("KOSPI constituents cache file not found.")

        return self.cache.read()
