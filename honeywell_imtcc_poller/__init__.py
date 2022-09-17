import click
import os

from .poller import Poller


@click.command()
@click.option(
    "-p",
    "--poll",
    default=None,
    flag_value=60,
    help="If specified, the tool will repeatedly poll, waiting the specified number of seconds between polls (default: 60).",
    is_flag=False,
    type=int,
)
def run_cli(poll):
    poller = Poller()
    poller.login(
        os.environ["HONEYWELL_EMAIL_ADDRESS"], os.environ["HONEYWELL_PASSWORD"]
    )
    poller.poll(wait=poll)
