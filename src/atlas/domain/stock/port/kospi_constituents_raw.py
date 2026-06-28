from typing import Protocol

import pandas as pd


class KospiConstituentsRawPort(Protocol):
    def read(self) -> pd.DataFrame:
        ...

    def exists(self) -> bool:
        ...