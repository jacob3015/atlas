import pandas as pd

from atlas.domain.etf.port.etf_master_cache import (
    EtfMasterCachePort,
)
from atlas.domain.etf.port.etf_master_raw import (
    EtfMasterRawPort,
)

class EtfMasterService:
    def __init__(
            self,
            raw: EtfMasterRawPort,
            cache: EtfMasterCachePort,
    ):
        self.raw = raw
        self.cache = cache

    def build(self) -> pd.DataFrame:
        if not self.raw.exists():
            raise FileNotFoundError("ETF raw file not found.")

        df = self.raw.read()
        self.cache.save(df)

        return df

    def read(self) -> pd.DataFrame:
        if not self.cache.exists():
            raise FileNotFoundError("ETF cache file not found.")

        return self.cache.read()