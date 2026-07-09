import typer


def register(app: typer.Typer) -> None:
    example_app = typer.Typer(help="Example commands.")

    @example_app.command()
    def hello(
            name: str = typer.Option(
                "Atlas",
                "--name",
                "-n",
                help="Name to greet.",
            ),
    ) -> None:
        """Print a greeting."""
        typer.echo(f"Hello, {name}!")

    app.add_typer(example_app, name="example")