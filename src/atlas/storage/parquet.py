from pathlib import Path

import pandas as pd


class EtfParquet:
    REQUIRED_COLUMNS = {
        "ticker",
        "name",
        "listing_date",
        "underlying_index",
        "leverage_type",
        "replication_method",
        "underlying_market",
        "asset_class",
        "expense_ratio",
        "tax_category",
    }

    OUTPUT_COLUMNS = [
        "ticker",
        "name",
        "listing_date",
        "underlying_index",
        "leverage_type",
        "replication_method",
        "underlying_market",
        "asset_class",
        "expense_ratio",
        "tax_category",
    ]

    def __init__(self, cache_path: Path):
        self.cache_path = cache_path

    def write(self, df: pd.DataFrame) -> None:
        self._validate(df)

        self.cache_path.parent.mkdir(parents=True, exist_ok=True)

        df = df.copy()
        df = df[self.OUTPUT_COLUMNS]

        df["ticker"] = df["ticker"].astype(str).str.zfill(6)

        for column in self.OUTPUT_COLUMNS:
            df[column] = df[column].astype(str).str.strip()

        df.to_parquet(self.cache_path, index=False)

    def read(self) -> pd.DataFrame:
        if not self.cache_path.exists():
            raise FileNotFoundError(f"ETF cache not found: {self.cache_path}")

        return pd.read_parquet(self.cache_path)

    def exists(self) -> bool:
        return self.cache_path.exists()

    def _validate(self, df: pd.DataFrame) -> None:
        missing = self.REQUIRED_COLUMNS - set(df.columns)

        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

class KospiParquet:
    REQUIRED_COLUMNS = {"ticker", "name"}

    def __init__(self, cache_path: Path):
        self.cache_path = cache_path

    def write(self, df: pd.DataFrame) -> None:
        self._validate(df)

        self.cache_path.parent.mkdir(parents=True, exist_ok=True)

        df = df.copy()
        df["ticker"] = df["ticker"].astype(str).str.zfill(6)
        df["name"] = df["name"].astype(str).str.strip()

        df.to_parquet(self.cache_path, index=False)

    def read(self) -> pd.DataFrame:
        if not self.cache_path.exists():
            raise FileNotFoundError(f"KOSPI constituents cache not found: {self.cache_path}")

        return pd.read_parquet(self.cache_path)

    def exists(self) -> bool:
        return self.cache_path.exists()

    def _validate(self, df: pd.DataFrame) -> None:
        missing = self.REQUIRED_COLUMNS - set(df.columns)

        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")