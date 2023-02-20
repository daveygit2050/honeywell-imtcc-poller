import httpretty
import pytest

from tests.simulators.honeywell_simulator import HoneywellSimulator
from tests.simulators.openweather_simulator import OpenWeatherSimulator
from tests.simulators.prometheus_simulator import PrometheusSimulator


@pytest.fixture(autouse=True)
def enable_httpretty_before_each_test():
    httpretty.enable(allow_net_connect=True)
    yield


@pytest.fixture(autouse=True)
def cleanup_httpretty_after_each_test():
    yield
    httpretty.reset()


@pytest.fixture
def honeywell_simulator():
    yield HoneywellSimulator()


@pytest.fixture
def openweather_simulator():
    yield OpenWeatherSimulator()


@pytest.fixture
def prometheus_simulator():
    yield PrometheusSimulator()
