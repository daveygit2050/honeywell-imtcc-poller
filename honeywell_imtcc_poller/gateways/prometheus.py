from typing import List

import prometheus_client


class Prometheus:
    def __init__(self) -> None:
        prometheus_client.start_http_server(8000)
        self.gauges = {}

    def add_gauge(self, name: str, description: str, labels: List[str]) -> None:
        self.gauges[name] = prometheus_client.Gauge(name, description, labels)

    def send_metric(self, gauge_name: str, labels: dict, value: float) -> None:
        self.gauges[gauge_name].labels(**labels).set(value)
