from pathlib import Path

from atlas.domain.stock.service.kospi_constituents import KospiConstituentsService
from atlas.infra.repository.cache.kospi_constituents import KospiConstituentsCacheRepository
from atlas.infra.repository.raw.kospi_constituents import KospiConstituentsRawRepository

from atlas.domain.etf.service.etf_master import EtfMasterService
from atlas.infra.repository.raw.etf_master import EtfMasterRawRepository
from atlas.infra.repository.cache.etf_master import EtfMasterCacheRepository


def create_kospi_constituents_service() -> KospiConstituentsService:
    raw = KospiConstituentsRawRepository(
        Path(".atlas/raw/stock/kospi-constituents")
    )

    cache = KospiConstituentsCacheRepository(
        Path(".atlas/cache/stock/kospi_constituents.parquet")
    )

    return KospiConstituentsService(raw=raw, cache=cache)

def create_etf_service() -> EtfMasterService:
    raw = EtfMasterRawRepository(
        Path(".atlas/raw/etf/master")
    )

    cache = EtfMasterCacheRepository(
        Path(".atlas/cache/etf/etf_master.parquet")
    )

    return EtfMasterService(raw=raw, cache=cache)