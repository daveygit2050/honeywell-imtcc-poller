import requests
import time
import socket

from tenacity import retry
from tenacity import wait_fixed


class Poller:
    def __init__(self, carbon_server_hostname):
        self.api_url = "https://international.mytotalconnectcomfort.com/api"
        self.session = requests.Session()
        self.carbon_server_hostname = carbon_server_hostname

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
            locations_response = self.session.get(f"{self.api_url}/locationsApi/getLocations")
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
                if zone["ThermostatType"] == 1:
                    self.send_metric(
                        "Hot Water", "current_temperature", zone["Temperature"]
                    )
                    continue
                self.send_metric(f"zone.{zone['Name']}", "current_temperature", zone["Temperature"])
            if wait:
                time.sleep(wait)
                continue
            return

    def send_metric(self, zone_name, metric_name, value) -> None:
        path = f"heating.{zone_name.replace(' ', '_').lower()}.{metric_name}"
        data = f"{path} {value} {int(time.time())}"
        print(data)
        if self.carbon_server_hostname:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as carbon_socket:
                carbon_socket.connect((self.carbon_server_hostname, 2003))
                carbon_socket.sendall(data.encode())
