import typer

from atlas import __version__
from atlas.cli.example import hello
from atlas.cli.stock import kospi_constituents


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

    hello.register(app)
    kospi_constituents.register(app)

    return app