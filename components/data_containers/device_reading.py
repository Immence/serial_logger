import time
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=False)
class DeviceReading:

    __slots__ = ("frequency", "temperature", "compensated", "sg")

    frequency : str
    temperature : str
    compensated : str
    sg : str
    gmt : str = field(init=False, default=datetime.now().strftime("%d/%m/%Y-%H:%M:%S"))
    unix_seconds : int = field(init=False, default=int(time.time()))

    def to_dict(self) -> dict:
        return {
            "frequency": self.frequency,
            "temperature": self.temperature,
            "compensated": self.compensated,
            "sg": self.sg
        }

@dataclass
class QcDeviceReading:

    __slots__ = ("frequency", "temperature", "compensated", "sg", "target_sg", "pass_threshold")

    frequency : str
    temperature : str
    compensated : str
    sg : str
    target_sg : str
    pass_threshold : str
    gmt : str = field(init=False, default=datetime.now().strftime("%d/%m/%Y-%H:%M:%S"))
    unix_seconds : int = field(init=False, default=int(time.time()))


    def deviance(self) -> float:
        if not self.target_sg:
            return None
        deviance = float(self.sg)-float(self.target_sg)
        return round(deviance, 6)

    def to_dict(self) -> dict:
        return {
            "frequency": self.frequency,
            "temperature": self.temperature,
            "compensated": self.compensated,
            "sg": self.sg,
            "target_sg" : self.target_sg,
            "pass_threshold": self.pass_threshold,
            "deviance": self.deviance()
        }
