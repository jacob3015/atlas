import keyring

from atlas.config.model import AtlasConfig


KEYRING_SERVICE_NAME = "atlas"
KRX_OPEN_API_AUTH_KEY_NAME = "krx-open-api-auth-key"


class SettingsError(RuntimeError):
    pass


class SettingLoader:
    def load(self) -> AtlasConfig:
        krx_open_api_auth_key = keyring.get_password(
            KEYRING_SERVICE_NAME,
            KRX_OPEN_API_AUTH_KEY_NAME,
        )

        if not krx_open_api_auth_key:
            raise SettingsError(
                "KRX OpenAPI authentication key is not configured.\n\n"
                "Register the authentication key first:\n\n"
                "    atlas config set krx-open-api-auth-key"
            )

        return AtlasConfig(
            krx_open_api_auth_key=krx_open_api_auth_key,
        )

class CredentialWriter:
    def set_krx_open_api_auth_key(self, auth_key: str) -> None:
        if not auth_key.strip():
            raise ValueError("KRX authentication key must not be empty.")

        keyring.set_password(
            KEYRING_SERVICE_NAME,
            KRX_OPEN_API_AUTH_KEY_NAME,
            auth_key.strip(),
        )
