import json
from datetime import datetime
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


class KrxKospiSeriesDailyPriceProvider:
    ENDPOINT = "https://data-dbg.krx.co.kr/svc/apis/idx/kospi_dd_trd"

    COLUMN_MAPPING = {
        "BAS_DD": "base_date",
        "IDX_CLSS": "index_class",
        "IDX_NM": "index_name",
        "CLSPRC_IDX": "close",
        "CMPPREVDD_IDX": "change",
        "FLUC_RT": "fluctuation_rate",
        "OPNPRC_IDX": "open",
        "HGPRC_IDX": "high",
        "LWPRC_IDX": "low",
        "ACC_TRDVOL": "trading_volume",
        "ACC_TRDVAL": "trading_value",
        "MKTCAP": "market_cap",
    }

    FLOAT_COLUMNS = [
        "close",
        "change",
        "fluctuation_rate",
        "open",
        "high",
        "low",
    ]

    INTEGER_COLUMNS = [
        "trading_volume",
        "trading_value",
        "market_cap",
    ]

    def __init__(self, auth_key: str):
        if not auth_key.strip():
            raise ValueError("KRX OpenAPI authentication key must not be empty.")

        self.auth_key = auth_key.strip()

    def read(self, base_date: str) -> pd.DataFrame:
        """Return KOSPI series daily prices for a YYYYMMDD base date."""
        self._validate_base_date(base_date)

        query = urlencode({"basDd": base_date})
        request = Request(
            url=f"{self.ENDPOINT}?{query}",
            headers={"AUTH_KEY": self.auth_key},
            method="GET",
        )

        with urlopen(request) as response:
            payload = json.load(response)

        return self._to_dataframe(payload)

    @staticmethod
    def _validate_base_date(base_date: str) -> None:
        try:
            parsed = datetime.strptime(base_date, "%Y%m%d")
        except (TypeError, ValueError) as exc:
            raise ValueError("base_date must be a valid date in YYYYMMDD format.") from exc

        if parsed.strftime("%Y%m%d") != base_date:
            raise ValueError("base_date must be a valid date in YYYYMMDD format.")

    def _to_dataframe(self, payload: Any) -> pd.DataFrame:
        if not isinstance(payload, dict):
            raise ValueError("Invalid KRX OpenAPI response: expected a JSON object.")

        records = payload.get("OutBlock_1")
        if not isinstance(records, list):
            raise ValueError(
                "Invalid KRX OpenAPI response: OutBlock_1 must be an array."
            )

        dataframe = pd.DataFrame(records)

        if dataframe.empty:
            return pd.DataFrame(columns=list(self.COLUMN_MAPPING.values()))

        missing = set(self.COLUMN_MAPPING) - set(dataframe.columns)
        if missing:
            raise ValueError(
                "Invalid KRX OpenAPI response: "
                f"missing fields: {sorted(missing)}"
            )

        dataframe = dataframe.rename(columns=self.COLUMN_MAPPING)
        dataframe = dataframe[list(self.COLUMN_MAPPING.values())]

        for column in self.FLOAT_COLUMNS:
            dataframe[column] = pd.to_numeric(dataframe[column], errors="coerce")

        for column in self.INTEGER_COLUMNS:
            dataframe[column] = pd.to_numeric(
                dataframe[column], errors="coerce"
            ).astype("Int64")

        return dataframe


class KrxKospiStockBasicInfoProvider:
    ENDPOINT = "https://data-dbg.krx.co.kr/svc/apis/sto/stk_isu_base_info"

    COLUMN_MAPPING = {
        "ISU_CD": "standard_code",
        "ISU_SRT_CD": "ticker",
        "ISU_NM": "full_name",
        "ISU_ABBRV": "name",
        "ISU_ENG_NM": "english_name",
        "LIST_DD": "listing_date",
        "MKT_TP_NM": "market_type",
        "SECUGRP_NM": "security_group",
        "SECT_TP_NM": "section_type",
        "KIND_STKCERT_TP_NM": "stock_type",
        "PARVAL": "par_value",
        "LIST_SHRS": "listed_shares",
    }

    def __init__(self, auth_key: str):
        if not auth_key.strip():
            raise ValueError("KRX OpenAPI authentication key must not be empty.")

        self.auth_key = auth_key.strip()

    def read(self, base_date: str) -> pd.DataFrame:
        """Return KOSPI stock basic information for a YYYYMMDD base date."""
        self._validate_base_date(base_date)

        query = urlencode({"basDd": base_date})
        request = Request(
            url=f"{self.ENDPOINT}?{query}",
            headers={"AUTH_KEY": self.auth_key},
            method="GET",
        )

        with urlopen(request) as response:
            payload = json.load(response)

        return self._to_dataframe(payload)

    @staticmethod
    def _validate_base_date(base_date: str) -> None:
        try:
            parsed = datetime.strptime(base_date, "%Y%m%d")
        except (TypeError, ValueError) as exc:
            raise ValueError("base_date must be a valid date in YYYYMMDD format.") from exc

        if parsed.strftime("%Y%m%d") != base_date:
            raise ValueError("base_date must be a valid date in YYYYMMDD format.")

    def _to_dataframe(self, payload: Any) -> pd.DataFrame:
        if not isinstance(payload, dict):
            raise ValueError("Invalid KRX OpenAPI response: expected a JSON object.")

        records = payload.get("OutBlock_1")
        if not isinstance(records, list):
            raise ValueError(
                "Invalid KRX OpenAPI response: OutBlock_1 must be an array."
            )

        dataframe = pd.DataFrame(records)

        if dataframe.empty:
            return pd.DataFrame(columns=list(self.COLUMN_MAPPING.values()))

        missing = set(self.COLUMN_MAPPING) - set(dataframe.columns)
        if missing:
            raise ValueError(
                "Invalid KRX OpenAPI response: "
                f"missing fields: {sorted(missing)}"
            )

        dataframe = dataframe.rename(columns=self.COLUMN_MAPPING)
        dataframe = dataframe[list(self.COLUMN_MAPPING.values())]

        string_columns = [
            column
            for column in self.COLUMN_MAPPING.values()
            if column != "listed_shares"
        ]
        for column in string_columns:
            dataframe[column] = dataframe[column].astype(str).str.strip()

        dataframe["ticker"] = dataframe["ticker"].str.zfill(6)
        dataframe["listed_shares"] = pd.to_numeric(
            dataframe["listed_shares"], errors="coerce"
        ).astype("Int64")

        return dataframe
