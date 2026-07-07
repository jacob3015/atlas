import pandas as pd

from atlas.domain.port.csv import (
    CsvPort,
)
from atlas.domain.port.parquet import (
    ParquetPort,
)

class KospiConstituentsService:
    def __init__(
            self,
            raw_port: CsvPort,
            cache_port: ParquetPort,
    ):
        self.raw_port = raw_port
        self.cache_port = cache_port

    def build(self) -> pd.DataFrame:
        if not self.raw_port.exists():
            raise FileNotFoundError("KOSPI constituents raw file not found.")

        df = self.raw_port.read()
        self.cache_port.save(df)

        return df

    def read(self) -> pd.DataFrame:
        if not self.cache_port.exists():
            raise FileNotFoundError("KOSPI constituents cache file not found.")

        return self.cache_port.read()