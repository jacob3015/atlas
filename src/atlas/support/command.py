import typer

from atlas.bootstrap import (
    create_etf_cache_service,
    create_kospi_cache_service
)

SUPPORTED_TARGETS = frozenset(["etf", "kospi"])

def register(app: typer.Typer) -> None:
    support_app = typer.Typer(help="Support commands.")

    @support_app.command()
    def build(target: str = typer.Option(..., "--target", "-t")) -> None:
        """Build cache for a target."""
        target = target.lower()
        if target not in SUPPORTED_TARGETS:
            raise typer.BadParameter("Currently only 'etf' and 'kospi' are supported as target.")

        if target == "etf":
            service = create_etf_cache_service()
        else:
            service = create_kospi_cache_service()

        try:
            df = service.build()
        except FileNotFoundError:
            typer.echo(f"Raw file not found for {target}.", err=True)
            raise typer.Exit(code=1)

        typer.echo(df.to_markdown(index=False))
        typer.echo(f"Cache built for {target}.")
        typer.echo(f"Rows: {len(df)}")

    @support_app.command()
    def read(target: str = typer.Option(..., "--target", "-t")) -> None:
        """Read cache for a target."""
        target = target.lower()
        if target not in SUPPORTED_TARGETS:
            raise typer.BadParameter("Currently only 'etf' and 'kospi' are supported as target.")

        if target == "etf":
            service = create_etf_cache_service()
        else:
            service = create_kospi_cache_service()

        try:
            df = service.read()
        except FileNotFoundError:
            typer.echo(f"Cache not found for {target}.", err=True)
            raise typer.Exit(code=1)

        typer.echo(df.to_markdown(index=False))
        typer.echo(f"Rows: {len(df)}")

    app.add_typer(support_app, name="support")