# KOSPI Constituents

This document explains how to prepare the raw KOSPI constituents data required by Atlas.

## Overview

Atlas does not download KOSPI constituents automatically.

The user is responsible for downloading the latest constituent list from the Korea Exchange (KRX) and placing it in the workspace.

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
    └── stock/
        └── kospi-constituents/
```

---

## Download

Download the KOSPI constituents list from the Korea Exchange (KRX).

Export the data as **CSV**.

The filename is **not important**.

Examples:

```text
KOSPI.csv
kospi-20260628.csv
constituents.csv
```

Atlas automatically loads the **most recently modified CSV file** in the directory.

---

## Place the File

Move the downloaded CSV into:

```text
.atlas/raw/stock/kospi-constituents/
```

Example:

```text
.atlas/
└── raw/
    └── stock/
        └── kospi-constituents/
            └── kospi-20260628.csv
```

---

## Build Cache

Generate the Parquet cache.

```bash
atlas kospi-constituents build
```

The cache will be created at:

```text
.atlas/
└── cache/
    └── stock/
        └── kospi_constituents.parquet
```

---

## Read Cache

Display the cached constituents.

```bash
atlas kospi-constituents read
```

---

## Notes

- Atlas automatically detects the latest CSV file by file metadata.
- The CSV filename does not need to follow a specific naming convention.
- The CSV is read with encoding detection to support files exported from KRX.