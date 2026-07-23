# About Support

This document describes how to use `atlas support` command.

## Contents

1. [Building ETF Cache](#building-etf-cache)
2. [Building KOSPI Cache](#building-kospi-cache)

## Building ETF Cache

### About ETF Cache

ETF Cache is a simple parquet cache for ETF ticker and name that are used in KRX.

### What for?

ETF Cache is used to resolve ETF name to ticker and vice versa in Atlas.

### How to build?

1. Download the raw csv from [KRX Data Marketplace](https://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030104).
2. Place the raw csv file in `.atlas/data/krx/etf` directory. The filename is not important.
3. Run `atlas support build --target etf`
4. The built parquet file will be placed in `.atlas/cache/etf/etf.parquet`.

## Building KOSPI Cache

### About KOSPI Cache

KOSPI Cache is a simple parquet cache for KOSPI constituents ticker and name.

### What for?

KOSPI Cache is used to resolve KOSPI constituents name to ticker and vice versa in Atlas.

### How to build?

1. Download the raw csv from [KRX Data Marketplace](https://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201010106).
2. Place the raw csv file in `.atlas/data/krx/kospi` directory. The filename is not important.
3. Run `atlas support build --target kospi`
4. The built parquet file will be placed in `.atlas/cache/kospi/kospi.parquet`.