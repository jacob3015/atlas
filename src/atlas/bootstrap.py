from pathlib import Path


from atlas.support.service import (
    EtfCacheService,
    KospiCacheService
)
from atlas.storage.csv import (
    EtfCsv,
    KospiCsv
)
from atlas.storage.parquet import (
    EtfParquet,
    KospiParquet
)

def create_etf_cache_service() -> EtfCacheService:
    raw_reader = EtfCsv(Path(".atlas/data/krx/etf"))
    cache_writer = EtfParquet(Path(".atlas/cache/etf/etf.parquet"))
    cache_reader = EtfParquet(Path(".atlas/cache/etf/etf.parquet"))

    return EtfCacheService(raw_reader=raw_reader, cache_writer=cache_writer, cache_reader=cache_reader)

def create_kospi_cache_service() -> KospiCacheService:
    raw_reader = KospiCsv(Path(".atlas/data/krx/kospi"))
    cache_writer = KospiParquet(Path(".atlas/cache/kospi/kospi.parquet"))
    cache_reader = KospiParquet(Path(".atlas/cache/kospi/kospi.parquet"))

    return KospiCacheService(raw_reader=raw_reader, cache_writer=cache_writer, cache_reader=cache_reader)