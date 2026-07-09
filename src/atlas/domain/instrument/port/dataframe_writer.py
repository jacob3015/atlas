from typing import Protocol

import pandas as pd


class DataFrameWriter(Protocol):
    def write(self, df: pd.DataFrame) -> None:
        ...

    def exists(self) -> bool:
        ...