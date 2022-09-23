import pytest

from tests.simulators.honeywell_simulator import HoneywellSimulator
from tests.simulators.openweather_simulator import OpenWeatherSimulator


@pytest.fixture
def honeywell_simulator():
    yield HoneywellSimulator()


@pytest.fixture
def openweather_simulator():
    yield OpenWeatherSimulator()
