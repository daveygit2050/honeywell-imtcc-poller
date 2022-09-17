import requests
import time
import prometheus_client


class Poller:
    def __init__(self):
        self.api_url = "https://international.mytotalconnectcomfort.com/api"
        self.session = requests.Session()
        prometheus_client.start_http_server(8000)
        self.current_temperature_guage = prometheus_client.Gauge(
            "current_temperature",
            f"Current temperature of a room or hot water system",
            ["zone_name", "is_hot_water"],
        )

    def login(self, email_address: str, password: str) -> None:
        login_data = {
            "EmailAddress": email_address,
            "Password": password,
            "RememberMe": False,
            "IsServiceStatusReturned": True,
            "ApiActive": True,
            "ApiDown": False,
            "RedirectUrl": "",
            "events": [],
            "formErrors": [],
        }
        login_response = self.session.post(
            f"{self.api_url}/accountApi/login",
            headers={"Content-Type": "application/json;charset=utf-8"},
            json=login_data,
        )
        login_response.raise_for_status()

    def poll(self, wait: int = None) -> None:
        while True:
            locations_response = self.session.get(
                f"{self.api_url}/locationsApi/getLocations"
            )
            locations_response.raise_for_status()
            location_id = locations_response.json()["Content"]["Locations"][0]["Id"]
            location_response = self.session.get(
                f"{self.api_url}/locationsApi/getLocationSystem?id={location_id}"
            )
            active_zones = [
                zone
                for zone in location_response.json()["Content"]["LocationModel"][
                    "Zones"
                ]
                if zone["IsAlive"]
            ]
            for zone in active_zones:
                is_hot_water = False
                zone_name = zone.get("Name")
                if zone["ThermostatType"] == 1:
                    is_hot_water = True
                    zone_name = "Hot Water"
                self.send_metric(zone_name, is_hot_water, zone["Temperature"])
            if wait:
                time.sleep(wait)
                continue
            return

    def send_metric(self, zone_name: str, is_hot_water: bool, value: float) -> None:
        print(f"{zone_name}: {value}")
        self.current_temperature_guage.labels(zone_name, is_hot_water).set(value)
