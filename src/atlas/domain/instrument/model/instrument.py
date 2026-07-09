from dataclasses import dataclass


@dataclass(frozen=True)
class Instrument:
    ticker: str
    name: str