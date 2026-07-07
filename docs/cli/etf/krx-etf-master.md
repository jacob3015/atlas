# ETF Master

This document explains how to prepare the raw ETF master data required by Atlas.

## Overview

Atlas does not download ETF master data automatically.

The user is responsible for downloading the latest ETF master dataset from the Korea Exchange (KRX) and placing it in the workspace.

This approach has the following advantages:

- No KRX account management is required.
- No dependency on third-party cached datasets.
- Users control when the master data is updated.

---

## Workspace

Create the following directory if it does not already exist.

```text
.atlas/
└── raw/
    └── etf/
        └── master/
```

---

## Download

Download the ETF master dataset from the Korea Exchange (KRX).

Export the data as **CSV**.

The filename is **not important**.

Examples:

```text
ETF.csv
etf-master-20260702.csv
master.csv
```

Atlas automatically loads the **most recently modified CSV file** in the directory.

---

## Place the File

Move the downloaded CSV into:

```text
.atlas/raw/etf/master/
```

Example:

```text
.atlas/
└── raw/
    └── etf/
        └── master/
            └── etf-master-20260702.csv
```

---

## Build Cache

Generate the Parquet cache.

```bash
atlas etf-master build
```

The cache will be created at:

```text
.atlas/
└── cache/
    └── etf/
        └── etf-master.parquet
```

---

## Read Cache

Display the cached ETF master data.

```bash
atlas etf-master read
```

---

## Dataset

The following fields are included in the cached dataset.

| Column | Description |
|---------|-------------|
| `ticker` | ETF ticker |
| `name` | ETF name |
| `listing_date` | Listing date |
| `underlying_index` | Underlying index |
| `leverage_type` | Leverage type |
| `replication_method` | Replication method |
| `underlying_market` | Underlying market |
| `asset_class` | Asset class |
| `expense_ratio` | Total expense ratio |
| `tax_category` | Tax category |

Atlas preserves the original values from the KRX dataset. Only the column names are normalized to English.

---

## Notes

- Atlas automatically detects the latest CSV file by file metadata.
- The CSV filename does not need to follow a specific naming convention.
- The CSV is read with encoding detection to support files exported from KRX.
- The original KRX values are preserved without translation.