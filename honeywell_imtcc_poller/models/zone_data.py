class ZoneData:
    def __init__(self, raw_zone_data: dict) -> None:
        self.current_temperature = raw_zone_data["Temperature"]
        self.desired_temperature = raw_zone_data["TargetHeatTemperature"]
        self.temperature_deficit = max(
            (self.desired_temperature - self.current_temperature), 0.0
        )
        self.type = "room"
        self.name = raw_zone_data.get("Name")

        if raw_zone_data["ThermostatType"] == 1:
            self.type = "water"
            self.name = "Hot Water"
