from typing import Protocol

import pandas as pd

class DataFrameReader(Protocol):
    def read(self) -> pd.DataFrame:
        ...

    def exists(self) -> bool:
        ...

class DataFrameWriter(Protocol):
    def write(self, df: pd.DataFrame) -> None:
        ...

    def exists(self) -> bool:
        ...