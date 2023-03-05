import os
import sys
import threading
import time
from typing import List

import honeywell_imtcc_poller


def execute_poller(mocker, additional_arguments: List[str] = None):
    sys_args = ["poll-honeywell"]
    if additional_arguments:
        sys_args.extend(additional_arguments)
    mocker.patch.object(sys, "argv", sys_args)

    polling_thread = threading.Thread(
        target=honeywell_imtcc_poller.run_cli, daemon=True
    )
    polling_thread.start()
    time.sleep(1)


def test_main(honeywell_simulator, openweather_simulator, prometheus_simulator, mocker):
    mocker.patch.dict(
        os.environ,
        {
            "HONEYWELL_EMAIL_ADDRESS": "foo@example.com",
            "HONEYWELL_PASSWORD": "foo-password",
            "OPENWEATHER_API_KEY": "foo-openweather-api-key",
            "OPENWEATHER_LATITUDE": "51.476852",
            "OPENWEATHER_LONGITUDE": "0.0005",
        },
    )

    execute_poller(mocker=mocker)

    prometheus_simulator.assert_gauge_added(
        name="current_temperature",
        description="Current temperature of a room or hot water system",
    )
    prometheus_simulator.assert_metric_sent(
        name="current_temperature",
        labels={"name": "Foo Room", "type": "room"},
        value=19.5,
    )
    prometheus_simulator.assert_metric_sent(
        name="current_temperature",
        labels={"name": "Hot Water", "type": "water"},
        value=49.0,
    )
    prometheus_simulator.assert_metric_sent(
        name="current_temperature",
        labels={"name": "Outside", "type": "outside"},
        value=16.36,
    )

    prometheus_simulator.assert_gauge_added(
        name="temperature_deficit",
        description="How many degrees are required for the room to reach target temperature",
    )
    prometheus_simulator.assert_metric_sent(
        name="temperature_deficit",
        labels={"name": "Foo Room", "type": "room"},
        value=2.0,
    )
    prometheus_simulator.assert_metric_sent(
        name="temperature_deficit",
        labels={"name": "Hot Water", "type": "water"},
        value=0.0,
    )


def test_arguments(mocker):
    mocker.patch.dict(
        os.environ,
        {
            "HONEYWELL_EMAIL_ADDRESS": "foo@example.com",
            "HONEYWELL_PASSWORD": "foo-password",
        },
    )

    mock_honeywell = mocker.patch("honeywell_imtcc_poller.Honeywell")
    mock_openweather = mocker.patch("honeywell_imtcc_poller.OpenWeather")
    mock_prometheus = mocker.patch("honeywell_imtcc_poller.Prometheus")

    execute_poller(mocker=mocker, additional_arguments=["--no-openweather"])

    mock_honeywell.assert_called()
    mock_prometheus.assert_called()
    mock_openweather.assert_not_called()
