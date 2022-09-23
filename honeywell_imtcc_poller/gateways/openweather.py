import requests


class OpenWeather:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get_temperature(self, latitude: float, longitude: float) -> float:
        response = requests.get(
            (
                "https://api.openweathermap.org/data/2.5/weather"
                f"?lat={latitude}"
                f"&lon={longitude}"
                "&units=metric"
                f"&appid={self.api_key}"
            )
        )
        response.raise_for_status()
        return response.json()["main"]["temp"]
