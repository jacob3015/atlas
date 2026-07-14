import pandas as pd

from atlas.storage.port import (
    DataFrameReader,
    DataFrameWriter,
)

class EtfCacheService:
    def __init__(
            self,
            raw_reader: DataFrameReader,
            cache_writer: DataFrameWriter,
            cache_reader: DataFrameReader
    ):
        self.raw_reader = raw_reader
        self.cache_writer = cache_writer
        self.cache_reader = cache_reader

    def build(self) -> pd.DataFrame:
        if not self.raw_reader.exists():
            raise FileNotFoundError("ETF raw file not found.")

        df = self.raw_reader.read()
        self.cache_writer.write(df)

        return df

    def read(self) -> pd.DataFrame:
        if not self.cache_reader.exists():
            raise FileNotFoundError("ETF cache file not found.")

        return self.cache_reader.read()

class KospiCacheService:
    def __init__(
            self,
            raw_reader: DataFrameReader,
            cache_writer: DataFrameWriter,
            cache_reader: DataFrameReader
    ):
        self.raw_reader = raw_reader
        self.cache_writer = cache_writer
        self.cache_reader = cache_reader

    def build(self) -> pd.DataFrame:
        if not self.raw_reader.exists():
            raise FileNotFoundError("KOSPI constituents raw file not found.")

        df = self.raw_reader.read()
        self.cache_writer.write(df)

        return df

    def read(self) -> pd.DataFrame:
        if not self.cache_reader.exists():
            raise FileNotFoundError("KOSPI constituents cache file not found.")

        return self.cache_reader.read()