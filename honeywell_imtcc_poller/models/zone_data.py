class ZoneData:
    def __init__(self, raw_zone_data: dict) -> None:
        self.current_temperature = raw_zone_data["Temperature"]
        self.is_hot_water = False
        self.name = raw_zone_data.get("Name")

        if raw_zone_data["ThermostatType"] == 1:
            self.is_hot_water = True
            self.name = "Hot Water"
