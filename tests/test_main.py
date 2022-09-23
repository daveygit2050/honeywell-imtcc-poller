import os
import sys
import threading
import time

import httpretty

import honeywell_imtcc_poller


def test_main(honeywell_simulator, mocker):
    mocker.patch.dict(
        os.environ,
        {
            "HONEYWELL_EMAIL_ADDRESS": "foo@example.com",
            "HONEYWELL_PASSWORD": "foo-password",
        },
    )
    mock_prometheus_client = mocker.patch(
        "honeywell_imtcc_poller.gateways.prometheus.prometheus_client"
    )
    httpretty.enable(allow_net_connect=False)
    mocker.patch.object(sys, "argv", ["poll-honeywell"])
    polling_thread = threading.Thread(
        target=honeywell_imtcc_poller.run_cli, daemon=True
    )
    polling_thread.start()
    time.sleep(1)
    assert [str(call) for call in mock_prometheus_client.mock_calls] == [
        "call.start_http_server(8000)",
        "call.Gauge('current_temperature', 'Current temperature of a room or hot water system', ['name', 'type'])",
        "call.Gauge().labels(name='Foo Room', type='room')",
        "call.Gauge().labels().set(19.5)",
        "call.Gauge().labels(name='Hot Water', type='water')",
        "call.Gauge().labels().set(49.0)",
    ]
