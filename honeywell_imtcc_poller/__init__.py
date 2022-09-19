import click
import os

from .poller import Poller


@click.command()
def run_cli():
    poller = Poller()
    poller.login(
        os.environ["HONEYWELL_EMAIL_ADDRESS"], os.environ["HONEYWELL_PASSWORD"]
    )
    poller.poll()
