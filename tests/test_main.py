import os
import sys
import threading
import time

import httpretty

import honeywell_imtcc_poller


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
    httpretty.enable(allow_net_connect=True)
    mocker.patch.object(sys, "argv", ["poll-honeywell"])

    polling_thread = threading.Thread(
        target=honeywell_imtcc_poller.run_cli, daemon=True
    )
    polling_thread.start()
    time.sleep(1)

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
