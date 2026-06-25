from atlas.cli.app import create_app


def main() -> None:
    app = create_app()
    app()


if __name__ == "__main__":
    main()