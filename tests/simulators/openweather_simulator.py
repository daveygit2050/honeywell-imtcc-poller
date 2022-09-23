import json

import httpretty


class OpenWeatherSimulator:
    def __init__(self) -> None:
        httpretty.register_uri(
            httpretty.GET,
            "https://api.openweathermap.org/data/2.5/weather?lat=51.476852&lon=0.0005&units=metric&appid=foo-openweather-api-key",
            body=json.dumps({"main": {"temp": 16.36}}),
            match_querystring=True,
        )
