from typing import List

import prometheus_client


class PrometheusSimulator:
    def assert_gauge_added(self, name: str, description: str):
        matching_metrics = [
            metric
            for metric in self.get_metrics(name=name)
            if metric.documentation == description
        ]
        assert (
            len(matching_metrics) > 0
        ), f"Found no gauge added with name={name} and description={description}"

    def assert_metric_sent(self, name: str, labels: dict, value: float):
        all_samples = []
        for metric in self.get_metrics(name=name):
            all_samples.extend(metric.samples)
        matching_samples = [
            sample
            for sample in all_samples
            if sample.labels == labels and sample.value == value
        ]
        assert (
            len(matching_samples) > 0
        ), f"Found no metric sent with name={name}, labels={labels} and value={value}"

    @staticmethod
    def get_metrics(name):
        return [
            metric
            for metric in prometheus_client.REGISTRY.collect()
            if metric.name == name
        ]
