import json
import re

import httpretty


class HoneywellSimulator:
    def __init__(self) -> None:
        api_uri = "https://international.mytotalconnectcomfort.com/api"
        canned_responses = {
            "/api/accountApi/login": {"FooLoginKey": "FooLoginValue"},
            "/api/locationsApi/getLocations": {
                "Content": {"Locations": [{"Id": "foo-location-id"}]}
            },
            "/api/locationsApi/getLocationSystem?id=foo-location-id": {
                "Content": {
                    "LocationModel": {
                        "Zones": [
                            {
                                "IsAlive": True,
                                "Name": "Foo Room",
                                "ThermostatType": 0,
                                "Temperature": 19.5,
                                "TargetHeatTemperature": 21.5,
                            },
                            {
                                "IsAlive": True,
                                "ThermostatType": 1,
                                "Temperature": 49.0,
                                "TargetHeatTemperature": 40.0,
                            },
                            {
                                "IsAlive": False,
                                "Name": "Dead Zone",
                                "ThermostatType": 0,
                                "Temperature": 5.0,
                                "TargetHeatTemperature": 5.0,
                            },
                        ]
                    }
                }
            },
        }

        def request_callback(request, uri, response_headers):
            response_status = 200
            try:
                response_body = json.dumps(canned_responses[request.path])
            except KeyError:
                response_body = b"Page not found"
                response_status = 404
            return [response_status, response_headers, response_body]

        for method in [httpretty.POST, httpretty.GET]:
            httpretty.register_uri(
                method,
                re.compile(rf"{api_uri}/.*"),
                body=request_callback,
            )
