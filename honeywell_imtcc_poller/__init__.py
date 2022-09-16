import click
import requests
import os

def main():
    api_url = "https://international.mytotalconnectcomfort.com/api"
    email_address = os.environ["HONEYWELL_EMAIL_ADDRESS"]
    password = os.environ["HONEYWELL_PASSWORD"]
    login_data = {
        "EmailAddress": email_address,
        "Password": password,
        "RememberMe": False,
        "IsServiceStatusReturned": True,
        "ApiActive": True,
        "ApiDown": False,
        "RedirectUrl": "",
        "events":[],
        "formErrors":[]
    }
    session = requests.Session()
    session.post(f"{api_url}/accountApi/login", headers={"Content-Type": "application/json;charset=utf-8"}, json=login_data)
    locations_response = session.get(f"{api_url}/locationsApi/getLocations")
    location_id = locations_response.json()["Content"]["Locations"][0]["Id"]
    location_response = session.get(f"{api_url}/locationsApi/getLocationSystem?id={location_id}")
    active_zones = [zone for zone in location_response.json()["Content"]["LocationModel"]["Zones"] if zone["IsAlive"]]
    for zone in active_zones:
        if zone["ThermostatType"] == 1:
            print(f"Hot Water: {zone['Temperature']}")
            continue
        print(f"{zone['Name']}: {zone['Temperature']}")


@click.command()
def run_cli():
    main()

