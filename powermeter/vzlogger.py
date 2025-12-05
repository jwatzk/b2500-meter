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
            return [int(self.get_json(self.uuid)["data"][0]["tuples"][0][1])]
        else:
            power_in = 0
            power_out = 0
            power_in = int(self.get_json(self.power_input_uuid)["data"][0]["tuples"][0][1])
            power_out = int(self.get_json(self.power_output_uuid)["data"][0]["tuples"][0][1])
            return [power_in - power_out]
