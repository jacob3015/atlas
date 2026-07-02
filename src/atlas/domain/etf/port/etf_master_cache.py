from typing import Protocol

import pandas as pd


class EtfCachePort(Protocol):
    def save(self, df: pd.DataFrame) -> None:
        ...

    def read(self) -> pd.DataFrame:
        ...

    def exists(self) -> bool:
        ...