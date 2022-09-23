import os
import time
from typing import List

import click

from .gateways.honeywell import Honeywell
from .gateways.prometheus import Prometheus


@click.command()
def run_cli():
    prometheus = Prometheus()
    prometheus.add_gauge(
        name="current_temperature",
        description="Current temperature of a room or hot water system",
        labels=["name", "type"],
    )

    honeywell = Honeywell(
        os.environ["HONEYWELL_EMAIL_ADDRESS"], os.environ["HONEYWELL_PASSWORD"]
    )
    location_ids = honeywell.get_location_ids()

    while True:
        update_metrics(honeywell, prometheus, location_ids)
        time.sleep(60)


def update_metrics(
    honeywell: Honeywell, prometheus: Prometheus, location_ids: List[str]
) -> None:
    zone_data = []
    for location_id in location_ids:
        zone_data.extend(honeywell.get_zone_data(location_id=location_id))
    for zone in zone_data:
        print(f"{zone.name}: {zone.current_temperature}")
        prometheus.send_metric(
            gauge_name="current_temperature",
            labels={
                "name": zone.name,
                "type": "water" if zone.is_hot_water else "room",
            },
            value=zone.current_temperature,
        )
