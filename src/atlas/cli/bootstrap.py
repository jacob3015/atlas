from pathlib import Path

from atlas.domain.index.service.kospi_constituents import KospiConstituentsService
from atlas.infra.repository.kospi_constituents_raw import KospiConstituentsRawRepository
from atlas.infra.repository.kospi_constituents_cache import KospiConstituentsCacheRepository

from atlas.domain.etf.service.krx_etf_master import KrxEtfMasterService
from atlas.infra.repository.krx_etf_master_raw import KrxEtfMasterRawRepository
from atlas.infra.repository.krx_etf_master_cache import KrxEtfMasterCacheRepository


def create_kospi_constituents_service() -> KospiConstituentsService:
    raw_port = KospiConstituentsRawRepository(
        Path(".atlas/data/kospi-constituents")
    )

    cache_port = KospiConstituentsCacheRepository(
        Path(".atlas/data/kospi-constituents/kospi_constituents.parquet")
    )

    return KospiConstituentsService(raw_port=raw_port, cache_port=cache_port)

def create_krx_etf_master_service() -> KrxEtfMasterService:
    raw_port = KrxEtfMasterRawRepository(
        Path(".atlas/data/krx-etf-master")
    )

    cache_port = KrxEtfMasterCacheRepository(
        Path(".atlas/data/krx-etf-master/krx_etf_master.parquet")
    )

    return KrxEtfMasterService(raw_port=raw_port, cache_port=cache_port)