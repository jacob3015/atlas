from dataclasses import dataclass


@dataclass(frozen=True)
class AtlasConfig:
    krx_open_api_auth_key: str