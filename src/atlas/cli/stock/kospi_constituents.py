import typer

from atlas.cli.bootstrap import create_kospi_constituents_service


def register(app: typer.Typer) -> None:
    kospi_app = typer.Typer(help="KOSPI constituents commands.")

    @kospi_app.command()
    def build() -> None:
        """Build KOSPI constituents cache from raw CSV."""
        service = create_kospi_constituents_service()
        df = service.build()

        typer.echo(df.to_markdown(index=False))
        typer.echo()
        typer.echo(f"Rows: {len(df)}")

    @kospi_app.command()
    def read() -> None:
        """Read KOSPI constituents cache."""
        service = create_kospi_constituents_service()
        df = service.read()

        typer.echo(df.to_markdown(index=False))
        typer.echo()
        typer.echo(f"Rows: {len(df)}")

    app.add_typer(kospi_app, name="kospi-constituents")