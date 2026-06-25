from atlas import __version__
from atlas.cli import hello

import typer


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

    return app