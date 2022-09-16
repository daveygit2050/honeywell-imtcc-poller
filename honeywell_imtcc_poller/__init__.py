import click
import os

from .poller import Poller


@click.command()
@click.option(
    "-c",
    "--carbon-server-hostname",
    default=None,
    flag_value="localhost",
    help="If specified, the tool will send metrics to a Carbon relay server the provided hostname (default: localhost).",
    is_flag=False,
    type=str,
)
@click.option(
    "-p",
    "--poll",
    default=None,
    flag_value=60,
    help="If specified, the tool will repeatedly poll, waiting the specified number of seconds between polls (default: 60).",
    is_flag=False,
    type=int,
)
def run_cli(carbon_server_hostname, poll):
    poller = Poller(carbon_server_hostname=carbon_server_hostname)
    poller.login(
        os.environ["HONEYWELL_EMAIL_ADDRESS"], os.environ["HONEYWELL_PASSWORD"]
    )
    poller.poll(wait=poll)
