from pathlib import Path

import pandas as pd


class KospiConstituentsRawRepository:
    ENCODINGS = ("cp949", "euc-kr", "utf-8-sig", "utf-8")

    REQUIRED_COLUMNS = {
        "종목코드",
        "종목명",
    }

    def __init__(self, raw_dir: Path):
        self.raw_dir = raw_dir

    def read(self) -> pd.DataFrame:
        csv_path = self._find_latest_csv()

        if csv_path is None:
            raise FileNotFoundError(
                f"No CSV files found in: {self.raw_dir}"
            )

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
                f"Invalid KOSPI constituents CSV: {csv_path}\n"
                f"Missing columns: {sorted(missing)}\n"
                f"Actual columns: {sorted(columns)}"
            )

    def _normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = [column.strip() for column in df.columns]

        result = df.rename(
            columns={
                "종목코드": "ticker",
                "종목명": "name",
            }
        )

        result = result[["ticker", "name"]]
        result["ticker"] = result["ticker"].str.zfill(6)
        result["name"] = result["name"].str.strip()

        return result