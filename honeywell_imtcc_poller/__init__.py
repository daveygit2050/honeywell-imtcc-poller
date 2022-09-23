import os
import time
from typing import List

import click

from .gateways import Honeywell
from .gateways import OpenWeather
from .gateways import Prometheus


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

    openweather = OpenWeather(api_key=os.environ["OPENWEATHER_API_KEY"])
    latitude = os.environ["OPENWEATHER_LATITUDE"]
    longitude = os.environ["OPENWEATHER_LONGITUDE"]

    while True:
        update_honeywell_metrics(honeywell, prometheus, location_ids)
        update_openweather_metrics(openweather, prometheus, latitude, longitude)
        time.sleep(60)


def update_honeywell_metrics(
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


def update_openweather_metrics(
    openweather: OpenWeather, prometheus: Prometheus, latitude: float, longitude: float
) -> None:
    outside_temperature = openweather.get_temperature(latitude, longitude)
    print(f"Outside: {outside_temperature}")
    prometheus.send_metric(
        gauge_name="current_temperature",
        labels={
            "name": "Outside",
            "type": "outside",
        },
        value=outside_temperature,
    )
