from pathlib import Path

from atlas.domain.stock.service.kospi_constituents import KospiConstituentsService
from atlas.infra.repository.cache.kospi_constituents import KospiConstituentsCacheRepository
from atlas.infra.repository.raw.kospi_constituents import KospiConstituentsRawRepository


def create_kospi_constituents_service() -> KospiConstituentsService:
    raw = KospiConstituentsRawRepository(
        Path(".atlas/raw/stock/kospi-constituents")
    )

    cache = KospiConstituentsCacheRepository(
        Path(".atlas/cache/stock/kospi_constituents.parquet")
    )

    return KospiConstituentsService(raw=raw, cache=cache)