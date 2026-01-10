from .base import Powermeter
import requests


class VZLogger(Powermeter):
    def __init__(
            self, 
            ip: str, 
            port: str, 
            uuid: str,
            power_calculate: bool,
            power_input_uuid: str,
            power_output_uuid: str,
        ):
        self.ip = ip
        self.port = port
        self.uuid = uuid
        self.power_calculate = power_calculate
        self.power_input_uuid = power_input_uuid
        self.power_output_uuid = power_output_uuid
        self.session = requests.Session()

    def get_json(self, path):        
        url = f"http://{self.ip}:{self.port}/{path}"
        return self.session.get(url, timeout=10).json()

    def get_powermeter_watts(self):
        if not self.power_calculate:
            try:
                data = self.get_json(self.uuid)
                value = data["data"][0]["tuples"][0][1]
                return [int(value)]
            except (KeyError, IndexError, ValueError) as e:
                raise ValueError(f"Failed to parse power value from VZLogger response: {e}") from e
        else:
            try:
                data_in = self.get_json(self.power_input_uuid)
                power_in = int(data_in["data"][0]["tuples"][0][1])
                
                data_out = self.get_json(self.power_output_uuid)
                power_out = int(data_out["data"][0]["tuples"][0][1])
                
                return [power_in - power_out]
            except (KeyError, IndexError, ValueError) as e:
                raise ValueError(f"Failed to parse power values from VZLogger response: {e}") from e
