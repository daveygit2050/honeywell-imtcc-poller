import pytest

from tests.simulators.honeywell_simulator import HoneywellSimulator


@pytest.fixture
def honeywell_simulator():
    yield HoneywellSimulator()
