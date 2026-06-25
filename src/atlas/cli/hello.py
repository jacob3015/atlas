import typer


def register(app: typer.Typer) -> None:
    @app.command()
    def hello(name: str) -> None:
        """Print a greeting."""
        typer.echo(f"Hello, {name}!")