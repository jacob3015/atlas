import typer

from atlas.cli.bootstrap import create_kospi_constituents_service


KOSPI_CONSTITUENTS_RAW_NOT_FOUND_MESSAGE = """
KOSPI constituents raw data not found.

Expected:
    
    .atlas/data/kospi-constituents/*.csv

Next steps:

1. Download the latest KOSPI constituents CSV from KRX.
2. Place the CSV in the directory above.
3. Run:

    atlas index stock constituents build --symbol kospi

See also:

    docs/cli/index/stock/kospi-constituents.md
""".strip()


KOSPI_CONSTITUENTS_CACHE_NOT_FOUND_MESSAGE = """
KOSPI constituents cache not found.

Build the cache first:

    atlas index stock constituents build --symbol kospi
""".strip()

def register(app: typer.Typer) -> None:
    index_app = typer.Typer(help="Index commands.")
    stock_app = typer.Typer(help="Stock index commands.")
    constituents_app = typer.Typer(help="Stock index constituents commands.")

    @constituents_app.command()
    def build(symbol: str = typer.Option(..., "--symbol", "-s")) -> None:
        """Build stock index constituents cache."""
        if symbol.lower() != "kospi":
            raise typer.BadParameter("Currently only 'kospi' is supported.")

        service = create_kospi_constituents_service()

        try:
            df = service.build()
        except FileNotFoundError:
            typer.echo(KOSPI_CONSTITUENTS_RAW_NOT_FOUND_MESSAGE, err=True)
            raise typer.Exit(code=1)

        typer.echo(df.to_markdown(index=False))
        typer.echo()
        typer.echo(f"Rows: {len(df)}")

    @constituents_app.command()
    def read(symbol: str = typer.Option(..., "--symbol", "-s")) -> None:
        """Read stock index constituents cache."""
        if symbol.lower() != "kospi":
            raise typer.BadParameter("Currently only 'kospi' is supported.")

        service = create_kospi_constituents_service()

        try:
            df = service.read()
        except FileNotFoundError:
            typer.echo(KOSPI_CONSTITUENTS_CACHE_NOT_FOUND_MESSAGE, err=True)
            raise typer.Exit(code=1)

        typer.echo(df.to_markdown(index=False))
        typer.echo()
        typer.echo(f"Rows: {len(df)}")

    stock_app.add_typer(constituents_app, name="constituents")
    index_app.add_typer(stock_app, name="stock")
    app.add_typer(index_app, name="index")