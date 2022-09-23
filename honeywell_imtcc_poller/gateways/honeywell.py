from typing import List

import requests

from honeywell_imtcc_poller.models import ZoneData


class Honeywell:
    def __init__(self, email_address: str, password: str) -> None:
        self.api_url = "https://international.mytotalconnectcomfort.com/api"
        self.session = requests.Session()
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

    def get_location_ids(self) -> List[str]:
        response = self.session.get(f"{self.api_url}/locationsApi/getLocations")
        response.raise_for_status()
        return [location["Id"] for location in response.json()["Content"]["Locations"]]

    def get_zone_data(self, location_id: str) -> List[ZoneData]:
        response = self.session.get(
            f"{self.api_url}/locationsApi/getLocationSystem?id={location_id}"
        )
        response.raise_for_status()
        return [
            ZoneData(zone)
            for zone in response.json()["Content"]["LocationModel"]["Zones"]
            if zone["IsAlive"]
        ]
