import typer

from atlas.config.service import CredentialWriter


def register(app: typer.Typer) -> None:
    config_app = typer.Typer(
        help="Atlas configuration commands.",
    )

    set_app = typer.Typer(
        help="Set Atlas configuration values.",
    )

    @set_app.command("krx-open-api-auth-key")
    def set_krx_open_api_auth_key() -> None:
        auth_key = typer.prompt(
            "KRX OpenAPI authentication key",
            hide_input=True,
            confirmation_prompt=True,
        )

        CredentialWriter().set_krx_open_api_auth_key(auth_key)

        typer.echo("KRX OpenAPI authentication key saved.")

    config_app.add_typer(set_app, name="set")
    app.add_typer(config_app, name="config")