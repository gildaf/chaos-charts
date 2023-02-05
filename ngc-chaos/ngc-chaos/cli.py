import typing
import typer
from probes import SanityParams, sanity_probe


app = typer.Typer()


@app.command()
def sanity(host: str = typer.Option(...), port: typing.Optional[int] = 6379):
    sanity_probe(SanityParams(host=host, port=port))


@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")
