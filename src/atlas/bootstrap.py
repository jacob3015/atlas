from pathlib import Path

from atlas.domain.index.service.kospi_constituents import KospiConstituentsService
from atlas.outbound.krx_kospi_constituents_csv import KrxKospiConstituentsCsvRepo
from atlas.outbound.krx_kospi_constituents_parquet import KrxKospiConstituentsParquetRepo

from atlas.domain.etf.service.krx_etf_master import KrxEtfMasterService
from atlas.outbound.krx_etf_master_csv import KrxEtfMasterCsvRepo
from atlas.outbound.krx_etf_master_parquet import KrxEtfMasterParquetRepo


def create_kospi_constituents_service() -> KospiConstituentsService:
    raw_reader = KrxKospiConstituentsCsvRepo(
        Path(".atlas/data/kospi-constituents")
    )

    cache_writer = KrxKospiConstituentsParquetRepo(
        Path(".atlas/data/kospi-constituents/kospi_constituents.parquet")
    )

    cache_reader = KrxKospiConstituentsParquetRepo(
        Path(".atlas/data/kospi-constituents/kospi_constituents.parquet")
    )

    return KospiConstituentsService(raw_reader=raw_reader, cache_writer=cache_writer, cache_reader=cache_reader)

def create_krx_etf_master_service() -> KrxEtfMasterService:
    raw_reader = KrxEtfMasterCsvRepo(
        Path(".atlas/data/krx-etf-master")
    )

    cache_writer = KrxEtfMasterParquetRepo(
        Path(".atlas/data/krx-etf-master/krx_etf_master.parquet")
    )

    cache_reader = KrxEtfMasterParquetRepo(
        Path(".atlas/data/krx-etf-master/krx_etf_master.parquet")
    )

    return KrxEtfMasterService(raw_reader=raw_reader, cache_writer=cache_writer, cache_reader=cache_reader)