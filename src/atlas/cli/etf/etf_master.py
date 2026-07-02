import typer

from atlas.cli.bootstrap import create_etf_service

RAW_NOT_FOUND_MESSAGE = """
ETF raw data not found.

Expected directory:
    .atlas/raw/etf/
    
Next steps:

1. Download the latest ETF data from KRX.
2. Place the CSV in the directory above.
3. Run:
    
    atlas etf build

See also:

    docs/cli/etf/etf-master.md
""".strip()

CACHE_NOT_FOUND_MESSAGE = """
ETF cache not found.

Build the cache first:

    atlas etf build
""".strip()

def register(app: typer.Typer) -> None:
    etf_app = typer.Typer(help="ETF commands.")

    @etf_app.command()
    def build() -> None:
        """Build ETF cache from raw CSV."""
        service = create_etf_service()

        try:
            df = service.build()
        except FileNotFoundError:
            typer.echo(RAW_NOT_FOUND_MESSAGE, err=True)
            raise typer.Exit(code=1)

        typer.echo(df.to_markdown(index=False))
        typer.echo()
        typer.echo(f"Rows: {len(df)}")

    @etf_app.command()
    def read() -> None:
        """Read ETF cache."""
        service = create_etf_service()

        try:
            df = service.read()
        except FileNotFoundError:
            typer.echo(CACHE_NOT_FOUND_MESSAGE, err=True)
            raise typer.Exit(code=1)

        typer.echo(df.to_markdown(index=False))
        typer.echo()
        typer.echo(f"Rows: {len(df)}")

    app.add_typer(etf_app, name="etf-master")