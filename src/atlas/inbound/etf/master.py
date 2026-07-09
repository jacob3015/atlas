import typer

from atlas.bootstrap import create_krx_etf_master_service

RAW_NOT_FOUND_MESSAGE = """
ETF raw data not found.

Expected:

    .atlas/data/krx-etf-master/*.csv
    
Next steps:

1. Download the latest ETF data from KRX.
2. Place the CSV in the directory above.
3. Run:
    
    atlas etf master build  --symbol krx

See also:

    docs/command/etf-master.md
""".strip()

CACHE_NOT_FOUND_MESSAGE = """
ETF cache not found.

Build the cache first:

    atlas etf master build --symbol krx
""".strip()

def register(app: typer.Typer) -> None:
    etf_app = typer.Typer(help="ETF commands.")
    master_app = typer.Typer(help="Master ETF commands.")

    @master_app.command()
    def build(symbol: str = typer.Option(..., "--symbol", "-s")) -> None:
        """Build ETF cache from raw CSV."""
        if symbol.lower() != "krx":
            raise typer.BadParameter("Currently only 'krx' is supported.")

        service = create_krx_etf_master_service()

        try:
            df = service.build()
        except FileNotFoundError:
            typer.echo(RAW_NOT_FOUND_MESSAGE, err=True)
            raise typer.Exit(code=1)

        typer.echo(df.to_markdown(index=False))
        typer.echo()
        typer.echo(f"Rows: {len(df)}")

    @master_app.command()
    def read(symbol: str = typer.Option(..., "--symbol", "-s")) -> None:
        """Read ETF cache."""
        if symbol.lower() != "krx":
            raise typer.BadParameter("Currently only 'krx' is supported.")

        service = create_krx_etf_master_service()

        try:
            df = service.read()
        except FileNotFoundError:
            typer.echo(CACHE_NOT_FOUND_MESSAGE, err=True)
            raise typer.Exit(code=1)

        typer.echo(df.to_markdown(index=False))
        typer.echo()
        typer.echo(f"Rows: {len(df)}")

    etf_app.add_typer(master_app, name="master")
    app.add_typer(etf_app, name="etf")