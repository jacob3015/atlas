import typer

from atlas.cli.bootstrap import create_kospi_constituents_service


RAW_NOT_FOUND_MESSAGE = """
KOSPI constituents raw data not found.

Expected directory:

    .atlas/raw/stock/kospi-constituents/

Next steps:

1. Download the latest KOSPI constituents CSV from KRX.
2. Place the CSV in the directory above.
3. Run:

    atlas kospi-constituents build

See also:

    docs/cli/stock/kospi-constituents.md
""".strip()


CACHE_NOT_FOUND_MESSAGE = """
KOSPI constituents cache not found.

Build the cache first:

    atlas kospi-constituents build
""".strip()


def register(app: typer.Typer) -> None:
    kospi_app = typer.Typer(help="KOSPI constituents commands.")

    @kospi_app.command()
    def build() -> None:
        """Build KOSPI constituents cache from raw CSV."""
        service = create_kospi_constituents_service()

        try:
            df = service.build()
        except FileNotFoundError:
            typer.echo(RAW_NOT_FOUND_MESSAGE, err=True)
            raise typer.Exit(code=1)

        typer.echo(df.to_markdown(index=False))
        typer.echo()
        typer.echo(f"Rows: {len(df)}")

    @kospi_app.command()
    def read() -> None:
        """Read KOSPI constituents cache."""
        service = create_kospi_constituents_service()

        try:
            df = service.read()
        except FileNotFoundError:
            typer.echo(CACHE_NOT_FOUND_MESSAGE, err=True)
            raise typer.Exit(code=1)

        typer.echo(df.to_markdown(index=False))
        typer.echo()
        typer.echo(f"Rows: {len(df)}")

    app.add_typer(kospi_app, name="kospi-constituents")