# KRX OpenAPI Authentication Key

This document explains how to configure the KRX OpenAPI authentication key required by Atlas.

## Overview

Some Atlas features use the Korea Exchange (KRX) OpenAPI to retrieve market data.

To access the KRX OpenAPI, an authentication key must first be issued by KRX and registered with Atlas.

Atlas stores the authentication key securely using the operating system credential store (for example, macOS Keychain).

The authentication key is never stored in the project directory or committed to version control.

---

## Prerequisites

Before configuring Atlas, obtain an authentication key from the KRX OpenAPI website.

KRX OpenAPI:

https://openapi.krx.co.kr/

---

## Register Authentication Key

Run the following command:

```shell
atlas config set krx-open-api-auth-key
```

Atlas will prompt for the authentication key.

```text
KRX OpenAPI authentication key:
Repeat for confirmation:
```

The input is hidden and will not be displayed on the terminal.

After successful registration:

```text
KRX OpenAPI authentication key saved.
```

Running the command again replaces the previously registered authentication key.

---

## Storage Location

Atlas stores the authentication key using the operating system credential store.

Examples:

- macOS → Keychain Access
- Windows → Credential Manager
- Linux → Secret Service compatible backend

The authentication key is not stored in:

```text
.atlas/
.env
pyproject.toml
git repository
```

---

## Verify Configuration

On macOS, the registered credential can be verified using Keychain Access.

Alternatively, from the terminal:

```shell
security find-generic-password -s atlas
```

Example output:

```text
keychain: "/Users/<user>/Library/Keychains/login.keychain-db"
class: "genp"
attributes:
    "acct"<blob>="krx-open-api-auth-key"
    "svce"<blob>="atlas"
```

The actual authentication key value is not displayed.

---

## Troubleshooting

### Authentication key is not configured

```text
KRX OpenAPI authentication key is not configured.

Run:

    atlas config set krx-open-api-auth-key
```

Register the authentication key and retry the command.

### Replace Existing Authentication Key

Simply execute the command again:

```shell
atlas config set krx-open-api-auth-key
```

The previously registered authentication key will be replaced.

---

## Security Notes

- Never commit authentication keys to Git repositories.
- Do not share authentication keys publicly.
- If the authentication key is exposed, revoke or reissue it through the KRX OpenAPI website and register the new key in Atlas.
