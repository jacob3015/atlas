import typer

from atlas import __version__
from atlas.support.command import register as support_register
from atlas.config.command import register as config_register


def create_app() -> typer.Typer:
    app = typer.Typer(invoke_without_command=True)

    @app.callback()
    def callback(
            version: bool = typer.Option(
                False,
                "--version",
                help="Show Atlas version and exit.",
                is_eager=True,
            ),
    ) -> None:
        if version:
            typer.echo(f"Atlas {__version__}")
            raise typer.Exit()

    support_register(app)
    config_register(app)

    return app