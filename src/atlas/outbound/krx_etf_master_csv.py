from pathlib import Path

import pandas as pd


class KrxEtfMasterCsvRepo:
    ENCODINGS = ("cp949", "euc-kr", "utf-8-sig", "utf-8")

    REQUIRED_COLUMNS = {
        "단축코드",
        "한글종목약명",
        "상장일",
        "기초지수명",
        "추적배수",
        "복제방법",
        "기초시장분류",
        "기초자산분류",
        "총보수",
        "과세유형",
    }

    COLUMN_MAPPING = {
        "단축코드": "ticker",
        "한글종목약명": "name",
        "상장일": "listing_date",
        "기초지수명": "underlying_index",
        "추적배수": "leverage_type",
        "복제방법": "replication_method",
        "기초시장분류": "underlying_market",
        "기초자산분류": "asset_class",
        "총보수": "expense_ratio",
        "과세유형": "tax_category",
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

    def __init__(self, raw_dir: Path):
        self.raw_dir = raw_dir

    def read(self) -> pd.DataFrame:
        csv_path = self._find_latest_csv()

        if csv_path is None:
            raise FileNotFoundError(f"No CSV files found in: {self.raw_dir}")

        df = self._read_csv(csv_path)
        self._validate(df, csv_path)

        return self._normalize(df)

    def exists(self) -> bool:
        return self._find_latest_csv() is not None

    def _find_latest_csv(self) -> Path | None:
        if not self.raw_dir.exists():
            return None

        csv_files = [
            path
            for path in self.raw_dir.glob("*.csv")
            if path.is_file()
        ]

        if not csv_files:
            return None

        return max(csv_files, key=lambda path: path.stat().st_mtime)

    def _read_csv(self, csv_path: Path) -> pd.DataFrame:
        last_error: Exception | None = None

        for encoding in self.ENCODINGS:
            try:
                return pd.read_csv(csv_path, encoding=encoding, dtype=str)
            except UnicodeDecodeError as exc:
                last_error = exc

        raise UnicodeDecodeError(
            "unknown",
            b"",
            0,
            1,
            f"Failed to decode CSV file: {csv_path}. Last error: {last_error}",
        )

    def _validate(self, df: pd.DataFrame, csv_path: Path) -> None:
        columns = {column.strip() for column in df.columns}
        missing = self.REQUIRED_COLUMNS - columns

        if missing:
            raise ValueError(
                f"Invalid ETF master CSV: {csv_path}\n"
                f"Missing columns: {sorted(missing)}\n"
                f"Actual columns: {sorted(columns)}"
            )

    def _normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = [column.strip() for column in df.columns]

        result = df.rename(columns=self.COLUMN_MAPPING)
        result = result[self.OUTPUT_COLUMNS]

        result["ticker"] = result["ticker"].astype(str).str.zfill(6)
        result["name"] = result["name"].astype(str).str.strip()

        for column in self.OUTPUT_COLUMNS:
            result[column] = result[column].astype(str).str.strip()

        return result